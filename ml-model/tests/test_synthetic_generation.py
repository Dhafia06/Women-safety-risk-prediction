import csv
import json
import tempfile
import unittest
from pathlib import Path

from data_generation.generate_synthetic_data import (
    DATASET_LABEL,
    HEADERS,
    REPORTING_UNITS,
    generate_records,
    generate_test_cases,
    write_synthetic_datasets,
)
from preprocessing.clean_data import clean_records
from preprocessing.config import load_config
from preprocessing.generate_report import build_report, write_reports
from preprocessing.inspect_data import inspect_csv
from preprocessing.utils import read_csv_rows, rows_to_dicts
from preprocessing.validate_data import validate_records


CONFIG = Path(__file__).parents[1] / "data_generation" / "synthetic_pipeline_config.json"


class SyntheticGenerationTests(unittest.TestCase):
    def test_generation_is_reproducible_and_clearly_labelled(self):
        first = generate_records()
        second = generate_records()
        self.assertEqual(first, second)
        self.assertEqual(len(first), 240)
        self.assertTrue(all(row["Dataset_Label"] == DATASET_LABEL for row in first))
        self.assertTrue(all(row["State"].startswith("SYNTH_STATE_") for row in first))
        scenarios = generate_test_cases()
        self.assertEqual(len(scenarios), 12)
        self.assertTrue(all(row["Dataset_Label"] == DATASET_LABEL for row in scenarios))
        self.assertEqual(
            {row["Scenario"] for row in scenarios},
            {
                "valid",
                "missing_count",
                "duplicate_exact",
                "invalid_numeric",
                "negative_count",
                "aggregate_like",
                "multiple_reporting_units",
                "ambiguous_geographical_key",
                "unexpected_category",
            },
        )
        self.assertEqual({row["Reporting_Unit"] for row in scenarios}, set(REPORTING_UNITS))

    def test_writer_creates_new_outputs_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dataset = root / "synthetic.csv"
            cases = root / "cases.csv"
            summary = write_synthetic_datasets(dataset, cases)
            self.assertEqual(summary["dataset_records"], 240)
            with self.assertRaises(FileExistsError):
                write_synthetic_datasets(dataset, cases)
            with dataset.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertTrue(rows)
            self.assertEqual(set(rows[0]), set(HEADERS))

    def test_scenario_fixture_runs_through_existing_pipeline_and_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dataset_path = root / "synthetic.csv"
            cases_path = root / "cases.csv"
            write_synthetic_datasets(dataset_path, cases_path)

            inspected = inspect_csv(
                cases_path,
                candidate_keys=[("Year", "State", "District", "Crime_Category")],
                categorical_fields=("Crime_Category", "Reporting_Unit", "Dataset_Label"),
                numeric_fields=("Year", "Crime_Count"),
                aggregate_indicators=("TOTAL", "ALL-AREA"),
            )
            self.assertEqual(inspected["row_count"], 12)
            self.assertGreaterEqual(inspected["duplicate_full_rows"]["groups"], 1)

            headers, raw_rows, _ = read_csv_rows(cases_path)
            records = rows_to_dicts(headers, raw_rows)
            cleaned = clean_records(records, load_config(CONFIG))
            self.assertEqual(len(cleaned.accepted), 10)
            self.assertEqual(len(cleaned.quarantined), 2)
            self.assertEqual(cleaned.original_count, len(cleaned.accepted) + len(cleaned.quarantined))
            self.assertTrue(any(row["Crime_Count"] == "" for row in cleaned.accepted))
            self.assertTrue(all(item["record"]["Dataset_Label"] == DATASET_LABEL for item in cleaned.quarantined))

            validation = validate_records(
                cleaned.accepted,
                load_config(CONFIG),
                headers=headers,
                original_count=cleaned.original_count,
                quarantined_count=len(cleaned.quarantined),
            )
            self.assertTrue(validation["valid"])
            self.assertEqual(validation["counts"]["aggregate_rows"], 1)
            issue_codes = {issue["code"] for issue in validation["issues"]}
            self.assertIn("record_count_preserved", issue_codes)
            self.assertIn("duplicate_candidate_keys", issue_codes)
            self.assertIn("unexpected_categories", issue_codes)

            report = build_report(
                inspected,
                validation,
                cleaned.summary(),
                config=load_config(CONFIG).to_dict(),
                execution_timestamp="2026-01-01T00:00:00+00:00",
            )
            json_path, markdown_path = root / "quality.json", root / "quality.md"
            write_reports(report, json_path, markdown_path)
            rendered = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(rendered["input"]["sha256"], inspected["sha256"])
            self.assertEqual(rendered["records"]["original_count"], 12)
            self.assertEqual(rendered["records"]["accepted_count"], 10)
            self.assertEqual(rendered["records"]["quarantined_count"], 2)
            self.assertTrue(markdown_path.is_file())


if __name__ == "__main__":
    unittest.main()
