"""Shared CSV, encoding, hashing, and no-overwrite file utilities."""

from __future__ import annotations

import codecs
import csv
import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any


class CsvReadError(ValueError):
    """CSV could not be decoded or parsed without losing source rows."""


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def detect_encoding(path: str | Path) -> tuple[str, str]:
    """Detect common Unicode BOMs or validate UTF-8; fallback is explicit."""

    path = Path(path)
    with path.open("rb") as stream:
        prefix = stream.read(4)
        if prefix.startswith(codecs.BOM_UTF8):
            return "utf-8-sig", "UTF-8 BOM detected"
        if prefix.startswith(codecs.BOM_UTF32_LE) or prefix.startswith(codecs.BOM_UTF32_BE):
            return "utf-32", "UTF-32 BOM detected"
        if prefix.startswith(codecs.BOM_UTF16_LE):
            return "utf-16", "UTF-16 little-endian BOM detected"
        if prefix.startswith(codecs.BOM_UTF16_BE):
            return "utf-16", "UTF-16 big-endian BOM detected"

    decoder = codecs.getincrementaldecoder("utf-8")("strict")
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                decoder.decode(chunk)
            decoder.decode(b"", final=True)
        return "utf-8", "Valid UTF-8; no BOM"
    except UnicodeDecodeError:
        return "cp1252", "UTF-8 validation failed; cp1252 fallback selected heuristically"


def read_csv_rows(path: str | Path) -> tuple[list[str], list[list[str]], dict[str, str]]:
    """Read a CSV without coercing cells; malformed input raises, never skips."""

    path = Path(path)
    encoding, encoding_note = detect_encoding(path)
    rows: list[list[str]] = []
    try:
        with path.open("r", encoding=encoding, errors="strict", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            for row in reader:
                rows.append(row)
    except (UnicodeError, csv.Error) as exc:
        raise CsvReadError(f"Unable to read CSV without loss: {exc}") from exc
    if not rows:
        raise CsvReadError("CSV is empty and has no header row")
    return rows[0], rows[1:], {"encoding": encoding, "encoding_note": encoding_note}


def rows_to_dicts(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> list[dict[str, str]]:
    if len(set(headers)) != len(headers):
        raise ValueError("Duplicate header names are ambiguous for record operations")
    records: list[dict[str, str]] = []
    for row_number, row in enumerate(rows, start=2):
        if len(row) != len(headers):
            raise ValueError(
                f"CSV row {row_number} has {len(row)} fields; expected {len(headers)}"
            )
        records.append(dict(zip(headers, row)))
    return records


def write_csv_new(
    path: str | Path,
    headers: Sequence[str],
    rows: Iterable[Sequence[Any]],
) -> None:
    """Write only to a new path; never replace an existing file."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)


def write_json_new(path: str | Path, value: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")


def ensure_distinct_new_paths(paths: Sequence[str | Path], inputs: Sequence[str | Path] = ()) -> None:
    resolved = [Path(path).resolve() for path in paths]
    if len(set(resolved)) != len(resolved):
        raise FileExistsError("Output paths must be distinct")
    input_paths = {Path(path).resolve() for path in inputs}
    if any(path in input_paths for path in resolved):
        raise ValueError("An output path cannot overwrite an input path")
    existing = [str(path) for path in resolved if path.exists()]
    if existing:
        raise FileExistsError("Refusing to overwrite existing output(s): " + ", ".join(existing))


def jsonable(value: Any) -> Any:
    """Convert common containers into JSON-compatible values deterministically."""

    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, set)):
        items = [jsonable(item) for item in value]
        return sorted(items, key=lambda item: json.dumps(item, sort_keys=True)) if isinstance(value, set) else items
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)
