import json
import tempfile
import unittest
from pathlib import Path

from preprocessing.clean_data import clean_records
from preprocessing.generate_report import build_report, render_markdown, write_reports
from preprocessing.inspect_data import inspect_csv
from preprocessing.validate_data import validate_records
from tests.support import FIXTURE, load_fixture, test_config


class GenerateReportTests(unittest.TestCase):
    def make_report(self):
        headers, records, _ = load_fixture()
        config = test_config()
        inspection = inspect_csv(FIXTURE, candidate_keys=config.candidate_keys, categorical_fields=config.categorical_fields, numeric_fields=("year", "count"), expected_values=config.allowed_categories)
        cleaning = clean_records(records, config)
        validation = validate_records(cleaning.accepted, config, headers=headers, original_count=len(records), quarantined_count=len(cleaning.quarantined))
        return build_report(
            inspection,
            validation,
            cleaning.summary(),
            config=config.to_dict(),
            execution_timestamp="2026-01-02T03:04:05+00:00",
            software={"test_mode": "artificial fixture"},
        )

    def test_report_contains_required_metadata_and_renders_markdown(self):
        report = self.make_report()
        self.assertEqual(report["input"]["row_count"], 12)
        self.assertEqual(report["records"]["quarantined_count"], 4)
        self.assertIn("validation", report)
        self.assertIn("duplicate_statistics", report)
        self.assertIn("missing_value_statistics", report)
        self.assertIn("transformation_audit", report)
        self.assertEqual(report["execution_timestamp_utc"], "2026-01-02T03:04:05+00:00")
        markdown = render_markdown(report)
        self.assertIn("Synthetic Pipeline Run Report", markdown)
        self.assertIn("Quarantined: 4", markdown)

    def test_json_and_markdown_outputs_are_new_only(self):
        report = self.make_report()
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path = Path(temp_dir) / "report.json"
            md_path = Path(temp_dir) / "report.md"
            write_reports(report, json_path, md_path)
            self.assertEqual(json.loads(json_path.read_text(encoding="utf-8")), report)
            self.assertTrue(md_path.read_text(encoding="utf-8").startswith("# Synthetic Pipeline Run Report"))
            with self.assertRaises(FileExistsError):
                write_reports(report, json_path, Path(temp_dir) / "another.md")

    def test_report_is_deterministic_for_fixed_inputs_and_timestamp(self):
        self.assertEqual(self.make_report(), self.make_report())


if __name__ == "__main__":
    unittest.main()
