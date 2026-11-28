"""Generate deterministic artificial annual records for software testing.

No project datasets are read. Labels and values are invented for pipeline
testing and do not represent Indian crime patterns or real places.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from typing import Sequence

from preprocessing.utils import write_csv_new


SEED = 20261128
DATASET_LABEL = "SYNTHETIC_ARTIFICIAL_ONLY_NOT_REAL_STATISTICS"
HEADERS = (
    "Year",
    "State",
    "District",
    "Crime_Category",
    "Crime_Count",
    "Reporting_Unit",
    "Scenario",
    "Dataset_Label",
)
SYNTHETIC_CATEGORIES = (
    "SYNTH_ASSAULT",
    "SYNTH_PROPERTY",
    "SYNTH_THEFT",
)
SCENARIO_CATEGORIES = SYNTHETIC_CATEGORIES + ("SYNTH_UNEXPECTED_CATEGORY",)
REPORTING_UNITS = ("SYNTH_REPORTING_UNIT_A", "SYNTH_REPORTING_UNIT_B")


def _record(
    year: str | int,
    state: str,
    district: str,
    category: str,
    count: str | int,
    reporting_unit: str,
    scenario: str,
) -> dict[str, str]:
    return {
        "Year": str(year),
        "State": state,
        "District": district,
        "Crime_Category": category,
        "Crime_Count": str(count),
        "Reporting_Unit": reporting_unit,
        "Scenario": scenario,
        "Dataset_Label": DATASET_LABEL,
    }


def generate_records(seed: int = SEED) -> list[dict[str, str]]:
    """Build 240 repeatable, valid artificial records with invented labels."""

    rng = random.Random(seed)
    records = []
    for year in range(2020, 2025):
        for state_number in range(1, 5):
            state = f"SYNTH_STATE_{state_number:02d}"
            for district_number in range(1, 5):
                district = f"SYNTH_DISTRICT_{state_number:02d}_{district_number:02d}"
                for category in SYNTHETIC_CATEGORIES:
                    reporting_unit = REPORTING_UNITS[(state_number + district_number + year) % 2]
                    records.append(
                        _record(
                            year,
                            state,
                            district,
                            category,
                            rng.randint(0, 250),
                            reporting_unit,
                            "valid_synthetic_record",
                        )
                    )
    return records


def generate_test_cases(seed: int = SEED) -> list[dict[str, str]]:
    """Build independent records covering each requested synthetic scenario."""

    rng = random.Random(seed ^ 0x5AFE)
    rows = [
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_VALID", "SYNTH_ASSAULT", rng.randint(1, 30), REPORTING_UNITS[0], "valid"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_MISSING", "SYNTH_THEFT", "", REPORTING_UNITS[0], "missing_count"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_DUPLICATE", "SYNTH_PROPERTY", 7, REPORTING_UNITS[0], "duplicate_exact"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_INVALID_NUMERIC", "SYNTH_ASSAULT", "not_a_number", REPORTING_UNITS[0], "invalid_numeric"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_NEGATIVE", "SYNTH_THEFT", -4, REPORTING_UNITS[0], "negative_count"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_TOTAL", "SYNTH_PROPERTY", 40, REPORTING_UNITS[0], "aggregate_like"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_MULTI_UNIT", "SYNTH_ASSAULT", 12, REPORTING_UNITS[0], "multiple_reporting_units"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_MULTI_UNIT", "SYNTH_ASSAULT", 9, REPORTING_UNITS[1], "multiple_reporting_units"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_AMBIGUOUS", "SYNTH_THEFT", 13, REPORTING_UNITS[0], "ambiguous_geographical_key"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_AMBIGUOUS", "SYNTH_THEFT", 15, REPORTING_UNITS[1], "ambiguous_geographical_key"),
        _record(2022, "SYNTH_STATE_CASE", "SYNTH_DISTRICT_UNEXPECTED", "SYNTH_UNEXPECTED_CATEGORY", 2, REPORTING_UNITS[0], "unexpected_category"),
    ]
    rows.append(dict(rows[2]))
    return rows


def write_synthetic_datasets(
    dataset_path: str | Path,
    test_cases_path: str | Path,
    *,
    seed: int = SEED,
) -> dict[str, int | str]:
    """Create two new CSVs only; existing outputs are never overwritten."""

    dataset_path = Path(dataset_path)
    test_cases_path = Path(test_cases_path)
    if dataset_path.resolve() == test_cases_path.resolve():
        raise ValueError("Synthetic dataset and scenario outputs must be different files")
    if dataset_path.exists() or test_cases_path.exists():
        existing = [str(path) for path in (dataset_path, test_cases_path) if path.exists()]
        raise FileExistsError("Refusing to overwrite synthetic output(s): " + ", ".join(existing))
    dataset_records = generate_records(seed)
    scenario_records = generate_test_cases(seed)
    write_csv_new(dataset_path, HEADERS, ([row[field] for field in HEADERS] for row in dataset_records))
    try:
        write_csv_new(test_cases_path, HEADERS, ([row[field] for field in HEADERS] for row in scenario_records))
    except OSError:
        # Never delete or replace an output. A partial pair is left visible for review.
        raise
    return {
        "seed": seed,
        "dataset_records": len(dataset_records),
        "test_case_records": len(scenario_records),
        "dataset_path": str(dataset_path),
        "test_cases_path": str(test_cases_path),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate clearly labelled artificial SafeHer pipeline data.")
    parser.add_argument("--dataset-output", default="dataset/synthetic/synthetic_crime_data.csv")
    parser.add_argument("--test-cases-output", default="dataset/synthetic/synthetic_test_cases.csv")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args(argv)
    try:
        import json

        summary = write_synthetic_datasets(args.dataset_output, args.test_cases_output, seed=args.seed)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
