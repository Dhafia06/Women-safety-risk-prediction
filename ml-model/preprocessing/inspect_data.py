"""Deterministic, read-only inspection of an explicitly supplied CSV."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Sequence

from .utils import detect_encoding, file_sha256


def _infer_type(values: list[str]) -> str:
    nonblank = [value for value in values if value.strip()]
    if not nonblank:
        return "empty"
    if all(value.strip().casefold() in {"true", "false"} for value in nonblank):
        return "boolean"
    parsed: list[Decimal] = []
    for value in nonblank:
        try:
            number = Decimal(value.strip())
        except InvalidOperation:
            return "text"
        if not number.is_finite():
            return "text/mixed"
        parsed.append(number)
    return "integer" if all(value == value.to_integral_value() for value in parsed) else "number"


def inspect_csv(
    path: str | Path,
    candidate_keys: Sequence[Sequence[str]] = (),
    categorical_fields: Sequence[str] = (),
    numeric_fields: Sequence[str] = (),
    expected_values: dict[str, Sequence[str]] | None = None,
    aggregate_indicators: Sequence[str] = ("total",),
    max_examples: int = 25,
) -> dict:
    """Return metadata and quality signals without altering or dropping rows.

    Blank strings are counted as missing. Other tokens such as ``NA`` remain
    literal values unless a caller later documents a source-specific rule.
    Aggregate detection is lexical and advisory only.
    """

    path = Path(path)
    metadata = path.stat()
    encoding, encoding_note = detect_encoding(path)
    headers: list[str] = []
    values_by_column: dict[str, list[str]] = defaultdict(list)
    full_rows: Counter[tuple[str, ...]] = Counter()
    key_counts: dict[str, Counter[tuple[str, ...]]] = {}
    for key in candidate_keys:
        key_counts["\u241f".join(key)] = Counter()
    invalid_widths: list[dict[str, int]] = []
    parse_issues: list[str] = []
    row_count = 0
    aggregate_rows: list[int] = []
    missing_counts: Counter[str] = Counter()
    invalid_values: dict[str, Counter[str]] = {name: Counter() for name in (expected_values or {})}

    try:
        with path.open("r", encoding=encoding, errors="strict", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            try:
                headers = next(reader)
            except StopIteration:
                return {
                    "file_name": path.name,
                    "file_path": str(path.resolve()),
                    "file_size_bytes": metadata.st_size,
                    "sha256": file_sha256(path),
                    "row_count": 0,
                    "column_count": 0,
                    "column_names": [],
                    "data_types": {},
                    "missing_values": {},
                    "duplicate_full_rows": {"groups": 0, "extra_occurrences": 0},
                    "duplicate_candidate_keys": {},
                    "unique_values": {},
                    "numeric_min_max": {},
                    "invalid_or_unexpected_values": {},
                    "potential_aggregate_rows": [],
                    "empty_columns": [],
                    "encoding": encoding,
                    "encoding_note": encoding_note,
                    "parsing_issues": ["CSV contains no header row"],
                }
            duplicate_headers = [name for name, count in Counter(headers).items() if count > 1]
            if duplicate_headers:
                parse_issues.append(f"Duplicate header names: {duplicate_headers!r}")
            known_names = set(headers)
            missing_configured = sorted(
                {name for group in candidate_keys for name in group if name not in known_names}
                | {name for name in categorical_fields if name not in known_names}
                | {name for name in numeric_fields if name not in known_names}
                | {name for name in (expected_values or {}) if name not in known_names}
            )
            if missing_configured:
                parse_issues.append(f"Configured columns absent from CSV: {missing_configured!r}")
            for data_row_number, row in enumerate(reader, start=1):
                row_count += 1
                if len(row) != len(headers):
                    if len(invalid_widths) < max_examples:
                        invalid_widths.append({"data_row": data_row_number, "field_count": len(row)})
                padded = row[: len(headers)] + [""] * max(0, len(headers) - len(row))
                full_rows[tuple(row)] += 1
                for name, value in zip(headers, padded):
                    values_by_column[name].append(value)
                    if value == "":
                        missing_counts[name] += 1
                    if name in invalid_values and value != "" and value not in (expected_values or {}).get(name, ()):
                        invalid_values[name][value] += 1
                row_map = dict(zip(headers, padded))
                for key in candidate_keys:
                    if all(name in row_map for name in key):
                        key_counts["\u241f".join(key)][tuple(row_map.get(name, "") for name in key)] += 1
                if any(
                    indicator.casefold() in cell.casefold()
                    for indicator in aggregate_indicators
                    if indicator
                    for cell in row
                ):
                    if len(aggregate_rows) < max_examples:
                        aggregate_rows.append(data_row_number)
    except (UnicodeError, csv.Error) as exc:
        parse_issues.append(f"CSV parsing/decoding stopped: {exc}")

    duplicate_key_summary = {}
    for key_name, counts in sorted(key_counts.items()):
        groups = [(key, count) for key, count in counts.items() if count > 1]
        duplicate_key_summary[key_name.replace("\u241f", ",")] = {
            "duplicate_groups": len(groups),
            "affected_rows": sum(count for _, count in groups),
            "extra_occurrences": sum(count - 1 for _, count in groups),
            "examples": [list(key) for key, _ in groups[:max_examples]],
        }

    numeric_min_max = {}
    for name in numeric_fields:
        if name not in values_by_column:
            continue
        parsed = []
        bad_values = Counter()
        for value in values_by_column[name]:
            if value == "":
                continue
            try:
                number = Decimal(value.strip())
                if not number.is_finite():
                    raise InvalidOperation
                parsed.append(number)
            except (InvalidOperation, ValueError):
                bad_values[value] += 1
        numeric_min_max[name] = {
            "minimum": str(min(parsed)) if parsed else None,
            "maximum": str(max(parsed)) if parsed else None,
            "non_numeric_values": dict(sorted(bad_values.items())[:max_examples]),
        }

    full_duplicate_groups = sum(1 for count in full_rows.values() if count > 1)
    full_duplicate_extras = sum(count - 1 for count in full_rows.values() if count > 1)
    return {
        "file_name": path.name,
        "file_path": str(path.resolve()),
        "file_size_bytes": metadata.st_size,
        "sha256": file_sha256(path),
        "row_count": row_count,
        "column_count": len(headers),
        "column_names": headers,
        "data_types": {name: _infer_type(values_by_column.get(name, [])) for name in headers},
        "missing_values": {
            name: {"count": missing_counts[name], "percent": round(missing_counts[name] * 100 / row_count, 4) if row_count else 0.0}
            for name in headers
        },
        "duplicate_full_rows": {"groups": full_duplicate_groups, "extra_occurrences": full_duplicate_extras},
        "duplicate_candidate_keys": duplicate_key_summary,
        "unique_values": {
            name: sorted(set(values_by_column[name]))[:max_examples]
            for name in categorical_fields if name in values_by_column
        },
        "numeric_min_max": numeric_min_max,
        "invalid_or_unexpected_values": {
            name: dict(sorted(counts.items())[:max_examples])
            for name, counts in invalid_values.items()
        } | {
            name: stats["non_numeric_values"]
            for name, stats in numeric_min_max.items() if stats["non_numeric_values"]
        },
        "potential_aggregate_rows": aggregate_rows,
        "potential_aggregate_row_count_at_least": len(aggregate_rows),
        "empty_columns": [name for name in headers if not any(v.strip() for v in values_by_column.get(name, []))],
        "row_width_issues": invalid_widths,
        "row_width_issue_count_at_least": len(invalid_widths),
        "encoding": encoding,
        "encoding_note": encoding_note,
        "parsing_issues": parse_issues,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect one explicitly supplied CSV read-only.")
    parser.add_argument("--input", required=True, help="Explicit CSV input path")
    parser.add_argument("--candidate-key", action="append", default=[], help="Comma-separated key columns; repeatable")
    parser.add_argument("--categorical-field", action="append", default=[])
    parser.add_argument("--numeric-field", action="append", default=[])
    parser.add_argument("--allowed-values", action="append", default=[], metavar="FIELD=VALUE1,VALUE2")
    parser.add_argument("--output-json", help="Optional new JSON report path; existing files are never overwritten")
    args = parser.parse_args(argv)
    expected_values = {}
    for entry in args.allowed_values:
        field, separator, values = entry.partition("=")
        if not separator:
            parser.error("--allowed-values must be FIELD=VALUE1,VALUE2")
        expected_values[field] = values.split(",")
    try:
        summary = inspect_csv(
            args.input,
            candidate_keys=[item.split(",") for item in args.candidate_key],
            categorical_fields=args.categorical_field,
            numeric_fields=args.numeric_field,
            expected_values=expected_values,
        )
        rendered = json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True)
        if args.output_json:
            output_path = Path(args.output_json)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered + "\n")
        else:
            print(rendered)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
