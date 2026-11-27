"""Structured validation; reports issues but never repairs or changes rows."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Sequence

from .config import DatasetConfig, load_config
from .utils import read_csv_rows, rows_to_dicts


SEVERITIES = {"ERROR", "WARNING", "INFO"}


def _issue(severity: str, code: str, message: str, **details: Any) -> dict[str, Any]:
    if severity not in SEVERITIES:
        raise ValueError(f"Unsupported severity: {severity}")
    return {"severity": severity, "code": code, "message": message, **details}


def validate_records(
    records: Sequence[dict[str, Any]],
    config: DatasetConfig,
    *,
    headers: Sequence[str] | None = None,
    original_count: int | None = None,
    quarantined_count: int = 0,
    expected_output_count: int | None = None,
) -> dict[str, Any]:
    """Validate in-memory records against only the supplied configuration."""

    issues: list[dict[str, Any]] = []
    actual_headers = list(headers if headers is not None else (records[0].keys() if records else ()))
    header_set = set(actual_headers)
    missing_columns = [name for name in config.required_columns if name not in header_set]
    if missing_columns:
        issues.append(_issue("ERROR", "required_columns_missing", "Required columns are absent", columns=missing_columns))
    if config.expected_columns:
        unexpected = [name for name in actual_headers if name not in config.expected_columns]
        missing_expected = [name for name in config.expected_columns if name not in header_set]
        if unexpected:
            issues.append(_issue("WARNING", "unexpected_columns", "Columns not listed in expected_columns were found", columns=unexpected))
        if missing_expected:
            issues.append(_issue("ERROR", "expected_columns_missing", "Expected columns are absent", columns=missing_expected))

    counts = {
        "records_checked": len(records),
        "missing_values_by_column": {},
        "duplicate_full_row_groups": 0,
        "duplicate_candidate_key_groups": {},
        "aggregate_rows": 0,
        "detail_rows": 0,
    }

    if records:
        for field in actual_headers:
            missing = sum(1 for record in records if record.get(field, "") == "" or record.get(field) is None)
            counts["missing_values_by_column"][field] = missing
            if missing:
                issues.append(_issue("WARNING", "missing_values", f"Blank/missing values found in {field}", field=field, count=missing))

    full_counter = Counter(tuple(record.get(field, "") for field in actual_headers) for record in records)
    counts["duplicate_full_row_groups"] = sum(1 for amount in full_counter.values() if amount > 1)
    if counts["duplicate_full_row_groups"]:
        issues.append(_issue("WARNING", "duplicate_full_rows", "Repeated full rows found; none were removed", groups=counts["duplicate_full_row_groups"]))

    for key in config.candidate_keys:
        if any(field not in header_set for field in key):
            issues.append(_issue("WARNING", "candidate_key_unavailable", "Configured candidate key could not be checked", key=list(key)))
            continue
        key_counter = Counter(tuple(record.get(field, "") for field in key) for record in records)
        duplicate_groups = [(values, amount) for values, amount in key_counter.items() if amount > 1]
        counts["duplicate_candidate_key_groups"]["|".join(key)] = len(duplicate_groups)
        if duplicate_groups:
            issues.append(_issue(
                "WARNING",
                "duplicate_candidate_keys",
                "Candidate key repeats were found; repeated keys are not automatically errors or removed",
                key=list(key),
                groups=len(duplicate_groups),
                affected_rows=sum(amount for _, amount in duplicate_groups),
                examples=[list(values) for values, _ in duplicate_groups[:10]],
            ))

    for field, kind in config.numeric_fields.items():
        if field not in header_set:
            issues.append(_issue("ERROR", "numeric_column_missing", "Configured numeric field is absent", field=field))
            continue
        for row_index, record in enumerate(records, start=2):
            value = record.get(field, "")
            if value == "" or value is None:
                continue
            try:
                numeric = Decimal(str(value).strip())
                if not numeric.is_finite():
                    raise InvalidOperation
                if kind in {"integer", "nonnegative_integer"} and numeric != numeric.to_integral_value():
                    raise InvalidOperation
            except (InvalidOperation, ValueError):
                issues.append(_issue("ERROR", "invalid_numeric", "Value is not a valid finite number for its configured type", field=field, row=row_index, value=str(value)))
                continue
            if kind in {"nonnegative_integer", "nonnegative_number"} and numeric < 0:
                issues.append(_issue("ERROR", "negative_count", "Configured nonnegative field contains a negative value", field=field, row=row_index, value=str(value)))
        if kind not in {"integer", "nonnegative_integer", "number", "nonnegative_number"}:
            issues.append(_issue("ERROR", "invalid_config_numeric_kind", "Unsupported numeric field kind", field=field, kind=kind))

    if config.year_field:
        if config.year_field not in header_set:
            issues.append(_issue("ERROR", "year_column_missing", "Configured year field is absent", field=config.year_field))
        else:
            for row_index, record in enumerate(records, start=2):
                value = record.get(config.year_field, "")
                if value == "" or value is None:
                    continue
                if not re.fullmatch(r"[+-]?\d+", str(value).strip()):
                    issues.append(_issue("ERROR", "invalid_year", "Year is not an integer", field=config.year_field, row=row_index, value=str(value)))
                    continue
                year = int(str(value).strip())
                if config.allowed_year_range:
                    start, end = config.allowed_year_range
                    if year < start or year > end:
                        issues.append(_issue("ERROR", "year_out_of_range", "Year falls outside the explicitly configured range", field=config.year_field, row=row_index, value=year, allowed=[start, end]))

    for field, allowed in config.allowed_categories.items():
        if field not in header_set:
            issues.append(_issue("WARNING", "category_column_missing", "Configured category field is absent", field=field))
            continue
        unexpected = Counter(str(record.get(field, "")) for record in records if record.get(field, "") not in allowed and record.get(field, "") != "")
        if unexpected:
            issues.append(_issue("WARNING", "unexpected_categories", "Values outside the explicitly configured vocabulary were found", field=field, values=dict(sorted(unexpected.items()))))

    def is_aggregate(record: dict[str, Any]) -> bool:
        if any(str(record.get(field, "")).strip().casefold() in {"total", "subtotal", "all india", "all-india"} for field in config.aggregate_fields if field in record):
            return True
        return any(
            indicator.casefold() in str(record.get(field, "")).casefold()
            for field in actual_headers
            for indicator in config.aggregate_indicators
            if indicator
        )

    counts["aggregate_rows"] = sum(is_aggregate(record) for record in records)
    counts["detail_rows"] = len(records) - counts["aggregate_rows"]
    if counts["aggregate_rows"] and counts["detail_rows"]:
        issues.append(_issue("WARNING", "aggregate_detail_mixed", "Potential aggregate and detail-like rows coexist; no row was removed", aggregate_rows=counts["aggregate_rows"], detail_rows=counts["detail_rows"]))
    elif counts["aggregate_rows"]:
        issues.append(_issue("INFO", "aggregate_rows_present", "Potential aggregate-like rows found; inspect their source definition", aggregate_rows=counts["aggregate_rows"]))

    if original_count is not None:
        preserved = len(records) + quarantined_count
        if preserved != original_count:
            issues.append(_issue("ERROR", "record_count_not_preserved", "Accepted plus quarantined record count differs from original", original_count=original_count, accepted_count=len(records), quarantined_count=quarantined_count, observed_preserved_count=preserved))
        else:
            issues.append(_issue("INFO", "record_count_preserved", "Accepted plus quarantined records match the original count", original_count=original_count, accepted_count=len(records), quarantined_count=quarantined_count))
    if expected_output_count is not None and len(records) != expected_output_count:
        issues.append(_issue("ERROR", "output_count_mismatch", "Output count differs from the explicit expected count", expected=expected_output_count, observed=len(records)))

    row_width_issues = [index for index, record in enumerate(records, start=2) if set(record) != header_set]
    if row_width_issues:
        issues.append(_issue("ERROR", "record_schema_inconsistent", "Record fields do not match the declared header", rows=row_width_issues[:25]))

    errors = sum(issue["severity"] == "ERROR" for issue in issues)
    warnings = sum(issue["severity"] == "WARNING" for issue in issues)
    return {
        "dataset_id": config.dataset_id,
        "valid": errors == 0,
        "counts": counts,
        "severity_counts": {"ERROR": errors, "WARNING": warnings, "INFO": len(issues) - errors - warnings},
        "issues": issues,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate one explicitly supplied CSV; does not repair it.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-json", help="Optional new JSON result path; existing files are never overwritten")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        headers, rows, _ = read_csv_rows(args.input)
        records = rows_to_dicts(headers, rows)
        result = validate_records(records, config, headers=headers)
        rendered = json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True)
        if args.output_json:
            output = Path(args.output_json)
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered + "\n")
        else:
            print(rendered)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
