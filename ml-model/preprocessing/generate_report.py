"""Create deterministic JSON and Markdown summaries from pipeline results."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from . import __version__
from .utils import ensure_distinct_new_paths, write_json_new


def build_report(
    inspection: dict[str, Any],
    validation: dict[str, Any],
    cleaning: dict[str, Any] | None = None,
    *,
    config: dict[str, Any] | None = None,
    execution_timestamp: str | None = None,
    software: dict[str, str] | None = None,
) -> dict[str, Any]:
    cleaning = cleaning or {}
    validation_issues = validation.get("issues", [])
    parse_issues = inspection.get("parsing_issues", [])
    issues = list(validation_issues) + [
        {"severity": "ERROR", "code": "csv_parse_issue", "message": item}
        for item in parse_issues
    ]
    return {
        "report_schema_version": "1.0",
        "execution_timestamp_utc": execution_timestamp or datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "preprocessing_package": __version__,
            **(software or {}),
        },
        "configuration": config or {},
        "input": {
            "file_name": inspection.get("file_name"),
            "file_path": inspection.get("file_path"),
            "size_bytes": inspection.get("file_size_bytes"),
            "sha256": inspection.get("sha256"),
            "encoding": inspection.get("encoding"),
            "encoding_note": inspection.get("encoding_note"),
            "row_count": inspection.get("row_count"),
            "column_count": inspection.get("column_count"),
            "column_names": inspection.get("column_names", []),
        },
        "records": {
            "original_count": cleaning.get("original_count", inspection.get("row_count", 0)),
            "output_count": cleaning.get("accepted_count", inspection.get("row_count", 0)),
            "accepted_count": cleaning.get("accepted_count", inspection.get("row_count", 0)),
            "quarantined_count": cleaning.get("quarantined_count", 0),
            "flagged_count": cleaning.get("flagged_count", 0),
            "preserved_count": cleaning.get("preserved_count", inspection.get("row_count", 0)),
            "record_count_preserved": cleaning.get("record_count_preserved", True),
        },
        "missing_value_statistics": inspection.get("missing_values", {}),
        "duplicate_statistics": {
            "full_rows": inspection.get("duplicate_full_rows", {}),
            "candidate_keys": inspection.get("duplicate_candidate_keys", {}),
        },
        "validation": validation,
        "transformation_audit": cleaning.get("transformation_audit", []),
        "quality_flags": cleaning.get("flags_by_source_row", {}),
        "errors": [item for item in issues if item.get("severity") == "ERROR"],
        "warnings": [item for item in issues if item.get("severity") == "WARNING"],
        "information": [item for item in issues if item.get("severity") == "INFO"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    inp = report.get("input", {})
    rec = report.get("records", {})
    validation = report.get("validation", {})
    lines = [
        "# Synthetic Pipeline Run Report",
        "",
        "> This report describes synthetic/artificial records only. It does not confer permission to process research datasets.",
        "",
        "## Input",
        "",
        f"- File: `{inp.get('file_name')}`",
        f"- Path: `{inp.get('file_path')}`",
        f"- Size: {inp.get('size_bytes')} bytes",
        f"- SHA-256: `{inp.get('sha256')}`",
        f"- Encoding: {inp.get('encoding')} ({inp.get('encoding_note')})",
        f"- Shape: {inp.get('row_count')} rows × {inp.get('column_count')} columns",
        f"- Columns: {', '.join(f'`{name}`' for name in inp.get('column_names', []))}",
        "",
        "## Record handling",
        "",
        f"- Original: {rec.get('original_count')}",
        f"- Accepted: {rec.get('accepted_count')}",
        f"- Quarantined: {rec.get('quarantined_count')}",
        f"- Flagged: {rec.get('flagged_count')}",
        f"- Count preserved: {rec.get('record_count_preserved')}",
        "",
        "## Validation",
        "",
        f"- Valid: {validation.get('valid')}",
        f"- Severity counts: `{json.dumps(validation.get('severity_counts', {}), sort_keys=True)}`",
        "",
        "### Issues",
        "",
    ]
    all_issues = validation.get("issues", [])
    if all_issues:
        for issue in all_issues:
            lines.append(f"- **{issue.get('severity')} / {issue.get('code')}**: {issue.get('message')}")
    else:
        lines.append("- None reported.")
    lines.extend([
        "",
        "## Transformations",
        "",
        f"- Audited transformation entries: {len(report.get('transformation_audit', []))}",
        "- Detailed audit and row flags are in the accompanying JSON report.",
        "",
        "## Execution",
        "",
        f"- UTC timestamp: `{report.get('execution_timestamp_utc')}`",
        f"- Software: `{json.dumps(report.get('software', {}), sort_keys=True)}`",
        "",
        "No geographic or crime-category mappings are inferred by this report generator.",
        "",
    ])
    return "\n".join(lines)


def write_reports(report: dict[str, Any], json_path: str | Path, markdown_path: str | Path) -> None:
    paths = [Path(json_path), Path(markdown_path)]
    ensure_distinct_new_paths(paths)
    # Preflight both paths to avoid knowingly creating a partial pair.
    for path in paths:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite existing report: {path}")
    write_json_new(paths[0], report)
    paths[1].parent.mkdir(parents=True, exist_ok=True)
    with paths[1].open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(render_markdown(report))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render JSON/Markdown reports from prior pipeline result JSON files.")
    parser.add_argument("--inspection-json", required=True)
    parser.add_argument("--validation-json", required=True)
    parser.add_argument("--cleaning-json", help="Optional audit JSON created by clean_data")
    parser.add_argument("--config-json", help="Optional configuration JSON to include in report")
    parser.add_argument("--json-output", required=True, help="New JSON destination; no overwrite")
    parser.add_argument("--markdown-output", required=True, help="New Markdown destination; no overwrite")
    args = parser.parse_args(argv)
    def read_json(path: str | None) -> dict[str, Any]:
        if path is None:
            return {}
        with Path(path).open("r", encoding="utf-8") as stream:
            value = json.load(stream)
        if not isinstance(value, dict):
            raise ValueError(f"Expected a JSON object in {path}")
        return value
    try:
        report = build_report(
            read_json(args.inspection_json),
            read_json(args.validation_json),
            read_json(args.cleaning_json),
            config=read_json(args.config_json),
        )
        write_reports(report, args.json_output, args.markdown_output)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
