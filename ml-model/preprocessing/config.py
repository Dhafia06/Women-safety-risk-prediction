"""Explicit, inert dataset configuration models.

No research-dataset mappings or cleaning rules are enabled in this module.
Configuration files are JSON so loading them does not add a dependency.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class QuarantineRule:
    """An opt-in exact-value rule that routes matching rows to quarantine."""

    rule_id: str
    field: str
    equals: str
    reason: str
    enabled: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "QuarantineRule":
        return cls(
            rule_id=str(value["rule_id"]),
            field=str(value["field"]),
            equals=str(value["equals"]),
            reason=str(value["reason"]),
            enabled=bool(value.get("enabled", False)),
        )


@dataclass(frozen=True)
class DatasetConfig:
    """Schema and policy supplied explicitly for one input dataset."""

    dataset_id: str
    required_columns: tuple[str, ...] = ()
    expected_columns: tuple[str, ...] = ()
    numeric_fields: dict[str, str] = field(default_factory=dict)
    candidate_keys: tuple[tuple[str, ...], ...] = ()
    year_field: str | None = None
    allowed_year_range: tuple[int, int] | None = None
    categorical_fields: tuple[str, ...] = ()
    allowed_categories: dict[str, tuple[str, ...]] = field(default_factory=dict)
    aggregate_fields: tuple[str, ...] = ()
    aggregate_indicators: tuple[str, ...] = ("total",)
    trim_fields: tuple[str, ...] = ()
    conversions: dict[str, str] = field(default_factory=dict)
    quarantine_rules: tuple[QuarantineRule, ...] = ()
    normalize_headers: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "DatasetConfig":
        year_range = value.get("allowed_year_range")
        if year_range is not None:
            if len(year_range) != 2:
                raise ValueError("allowed_year_range must contain [minimum, maximum]")
            year_range = (int(year_range[0]), int(year_range[1]))
        return cls(
            dataset_id=str(value["dataset_id"]),
            required_columns=tuple(value.get("required_columns", ())),
            expected_columns=tuple(value.get("expected_columns", ())),
            numeric_fields=dict(value.get("numeric_fields", {})),
            candidate_keys=tuple(tuple(key) for key in value.get("candidate_keys", ())),
            year_field=value.get("year_field"),
            allowed_year_range=year_range,
            categorical_fields=tuple(value.get("categorical_fields", ())),
            allowed_categories={
                name: tuple(values)
                for name, values in value.get("allowed_categories", {}).items()
            },
            aggregate_fields=tuple(value.get("aggregate_fields", ())),
            aggregate_indicators=tuple(value.get("aggregate_indicators", ("total",))),
            trim_fields=tuple(value.get("trim_fields", ())),
            conversions=dict(value.get("conversions", {})),
            quarantine_rules=tuple(
                QuarantineRule.from_dict(rule)
                for rule in value.get("quarantine_rules", ())
            ),
            normalize_headers=bool(value.get("normalize_headers", False)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "required_columns": list(self.required_columns),
            "expected_columns": list(self.expected_columns),
            "numeric_fields": dict(sorted(self.numeric_fields.items())),
            "candidate_keys": [list(key) for key in self.candidate_keys],
            "year_field": self.year_field,
            "allowed_year_range": (
                list(self.allowed_year_range) if self.allowed_year_range else None
            ),
            "categorical_fields": list(self.categorical_fields),
            "allowed_categories": {
                key: list(values)
                for key, values in sorted(self.allowed_categories.items())
            },
            "aggregate_fields": list(self.aggregate_fields),
            "aggregate_indicators": list(self.aggregate_indicators),
            "trim_fields": list(self.trim_fields),
            "conversions": dict(sorted(self.conversions.items())),
            "quarantine_rules": [rule.__dict__ for rule in self.quarantine_rules],
            "normalize_headers": self.normalize_headers,
        }


def load_config(path: str | Path) -> DatasetConfig:
    """Load a caller-supplied JSON config; no project dataset config is implicit."""

    with Path(path).open("r", encoding="utf-8") as stream:
        raw = json.load(stream)
    if not isinstance(raw, dict) or not raw.get("dataset_id"):
        raise ValueError("Config JSON must be an object with a non-empty dataset_id")
    return DatasetConfig.from_dict(raw)


def normalize_header_name(label: str) -> str:
    """Return a reversible-by-audit comparison name; never apply implicitly."""

    import re

    normalized = re.sub(r"[^0-9A-Za-z]+", "_", label.strip()).strip("_").lower()
    return normalized or "unnamed_column"


def normalized_header_mapping(headers: tuple[str, ...] | list[str]) -> dict[str, str]:
    """Map original headers to safe names, rejecting collisions."""

    if len(headers) != len(set(headers)):
        raise ValueError("Duplicate original headers are ambiguous; preserve them as a positional schema")
    mapping = {header: normalize_header_name(header) for header in headers}
    values = list(mapping.values())
    if len(values) != len(set(values)):
        raise ValueError("Header normalization would collide; preserve original headers")
    return mapping
