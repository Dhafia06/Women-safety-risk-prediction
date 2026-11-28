"""Opt-in, auditable row cleaning that never silently drops source records."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Sequence

from .config import DatasetConfig, load_config, normalized_header_mapping
from .utils import (
    ensure_distinct_new_paths,
    read_csv_rows,
    rows_to_dicts,
    write_csv_new,
    write_json_new,
)


@dataclass
class CleaningResult:
    accepted: list[dict[str, Any]]
    quarantined: list[dict[str, Any]]
    flags: dict[int, list[str]]
    transformation_audit: list[dict[str, Any]]
    original_count: int
    header_mapping: dict[str, str]

    @property
    def flagged_count(self) -> int:
        return sum(bool(items) for items in self.flags.values())

    def summary(self) -> dict[str, Any]:
        return {
            "original_count": self.original_count,
            "accepted_count": len(self.accepted),
            "quarantined_count": len(self.quarantined),
            "flagged_count": self.flagged_count,
            "preserved_count": len(self.accepted) + len(self.quarantined),
            "record_count_preserved": len(self.accepted) + len(self.quarantined) == self.original_count,
            "transformation_audit": self.transformation_audit,
            "flags_by_source_row": {str(k): v for k, v in sorted(self.flags.items())},
            "header_mapping": self.header_mapping,
        }


def _coerce(value: str, kind: str) -> Any:
    if kind == "integer":
        parsed = Decimal(value.strip())
        if not parsed.is_finite() or parsed != parsed.to_integral_value():
            raise ValueError("not a finite integer")
        return int(parsed)
    if kind == "number":
        parsed = Decimal(value.strip())
        if not parsed.is_finite():
            raise ValueError("not a finite number")
        return float(parsed)
    if kind == "text":
        return value
    raise ValueError(f"unsupported conversion kind: {kind}")


def clean_records(records: Sequence[dict[str, Any]], config: DatasetConfig) -> CleaningResult:
    """Apply only explicitly configured transformations and quarantine rules.

    Every source row is returned in exactly one of ``accepted`` or
    ``quarantined``. Quarantined rows carry source-row, reason, and flag
    metadata while the original cell values are retained in ``record``.
    No rule deletes, merges, averages, or imputes values.
    """

    source_headers = tuple(records[0].keys()) if records else tuple(config.expected_columns)
    header_mapping = normalized_header_mapping(source_headers) if config.normalize_headers else {
        header: header for header in source_headers
    }
    output_keys = list(header_mapping.values())
    if len(set(output_keys)) != len(output_keys):
        raise ValueError("Configured safe header names collide; refusing to clean")

    accepted: list[dict[str, Any]] = []
    quarantined: list[dict[str, Any]] = []
    flags: dict[int, list[str]] = defaultdict(list)
    audit: list[dict[str, Any]] = []
    records_for_checks: dict[int, dict[str, Any]] = {}
    rule_by_id = {rule.rule_id: rule for rule in config.quarantine_rules}

    for row_number, source in enumerate(records, start=2):
        current = deepcopy(source)
        row_changes = []
        reasons = []
        for field in config.trim_fields:
            if field not in current:
                continue
            value = current[field]
            if isinstance(value, str) and value != value.strip():
                trimmed = value.strip()
                row_changes.append({"field": field, "operation": "trim_outer_whitespace", "original": value, "result": trimmed})
                current[field] = trimmed

        for field, kind in config.conversions.items():
            if field not in current:
                continue
            original = current[field]
            if original == "":
                continue  # Missing remains missing; never turn it into zero.
            try:
                converted = _coerce(str(original), kind)
            except (ValueError, InvalidOperation) as exc:
                reasons.append(f"invalid_conversion:{field}:{exc}")
                continue
            if converted != original or type(converted) is not type(original):
                row_changes.append({"field": field, "operation": f"convert_to_{kind}", "original": original, "result": converted})
                current[field] = converted

        for field, kind in config.numeric_fields.items():
            if field not in current or current[field] == "":
                continue
            value = current[field]
            try:
                parsed = Decimal(str(value).strip())
                if not parsed.is_finite():
                    raise InvalidOperation
                if kind in {"integer", "nonnegative_integer"} and parsed != parsed.to_integral_value():
                    raise InvalidOperation
                if kind in {"nonnegative_integer", "nonnegative_number"} and parsed < 0:
                    reasons.append(f"negative_value:{field}")
            except (InvalidOperation, ValueError):
                reasons.append(f"invalid_numeric_value:{field}")

        if config.year_field and config.year_field in current and current[config.year_field] != "":
            try:
                year = int(str(current[config.year_field]).strip())
                if config.allowed_year_range:
                    start, end = config.allowed_year_range
                    if year < start or year > end:
                        reasons.append(f"year_out_of_range:{config.year_field}")
            except (TypeError, ValueError):
                reasons.append(f"invalid_year:{config.year_field}")

        for field, allowed in config.allowed_categories.items():
            if field in current and current[field] != "" and current[field] not in allowed:
                flags[row_number].append(f"unexpected_category:{field}")

        for rule in config.quarantine_rules:
            if not rule.enabled:
                continue
            if rule.field in current and str(current[rule.field]) == rule.equals:
                reasons.append(f"{rule.rule_id}:{rule.reason}")

        if row_changes:
            audit.append({"source_row_number": row_number, "changes": row_changes})

        if config.normalize_headers:
            output_record = {header_mapping[key]: value for key, value in current.items()}
        else:
            output_record = current
        records_for_checks[row_number] = current

        if reasons:
            flags[row_number].extend(reasons)
            quarantined.append({
                "source_row_number": row_number,
                "record": output_record,
                "reasons": reasons,
                "flags": list(flags[row_number]),
            })
        else:
            accepted.append(output_record)

    # Duplicate detection is informative and non-destructive across all rows.
    full_groups: dict[tuple, list[int]] = defaultdict(list)
    key_groups: dict[tuple[str, tuple], list[int]] = defaultdict(list)
    for row_number, source in records_for_checks.items():
        full_groups[tuple(source.values())].append(row_number)
        for key in config.candidate_keys:
            if all(field in source for field in key):
                key_groups[("\u241f".join(key), tuple(source[field] for field in key))].append(row_number)
    for group in full_groups.values():
        if len(group) > 1:
            for row_number in group:
                flags[row_number].append("duplicate_full_row")
    for (key_name, _), group in key_groups.items():
        if len(group) > 1:
            marker = "duplicate_candidate_key:" + key_name
            for row_number in group:
                flags[row_number].append(marker)

    # Refresh quarantined sidecar flags with duplicate findings.
    for item in quarantined:
        item["flags"] = list(dict.fromkeys(flags[item["source_row_number"]]))
    return CleaningResult(
        accepted=accepted,
        quarantined=quarantined,
        flags={key: list(dict.fromkeys(value)) for key, value in flags.items()},
        transformation_audit=audit,
        original_count=len(records),
        header_mapping=header_mapping,
    )


def _write_result(result: CleaningResult, output: Path, quarantine_output: Path, audit_output: Path) -> None:
    ensure_distinct_new_paths([output, quarantine_output, audit_output])
    accepted_headers = list(result.accepted[0].keys()) if result.accepted else list(result.header_mapping.values())
    if result.quarantined:
        quarantine_headers = accepted_headers + ["__quarantine_reasons", "__quality_flags", "__source_row_number"]
    else:
        quarantine_headers = accepted_headers + ["__quarantine_reasons", "__quality_flags", "__source_row_number"]
    # Check all targets before opening any one of them.
    for target in (output, quarantine_output, audit_output):
        if target.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {target}")
    write_csv_new(output, accepted_headers, ([record.get(field, "") for field in accepted_headers] for record in result.accepted))
    write_csv_new(
        quarantine_output,
        quarantine_headers,
        (
            [item["record"].get(field, "") for field in accepted_headers]
            + ["; ".join(item["reasons"]), "; ".join(item["flags"]), item["source_row_number"]]
            for item in result.quarantined
        ),
    )
    write_json_new(audit_output, result.summary())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Clean an explicitly supplied CSV with an explicit JSON config.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--write", action="store_true", help="Write outputs; default is dry-run")
    parser.add_argument("--output", help="New accepted CSV path; required with --write")
    parser.add_argument("--quarantine-output", help="New quarantine CSV path; required with --write")
    parser.add_argument("--audit-output", help="New audit JSON path; required with --write")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        headers, rows, _ = read_csv_rows(args.input)
        records = rows_to_dicts(headers, rows)
        result = clean_records(records, config)
        summary = result.summary()
        if args.write:
            if not (args.output and args.quarantine_output and args.audit_output):
                parser.error("--write requires --output, --quarantine-output, and --audit-output")
            _write_result(result, Path(args.output), Path(args.quarantine_output), Path(args.audit_output))
            summary["outputs_written"] = True
        else:
            if args.output or args.quarantine_output or args.audit_output:
                parser.error("Output paths are accepted only with --write; default mode is dry-run")
            summary["dry_run"] = True
            summary["outputs_written"] = False
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    # ASCII escaping keeps JSON printable in Windows consoles using legacy code pages.
    print(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
