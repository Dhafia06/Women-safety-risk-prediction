import tempfile
import unittest
from pathlib import Path

from preprocessing.inspect_data import inspect_csv
from preprocessing.utils import CsvReadError
from tests.support import FIXTURE, load_fixture, test_config


class InspectDataTests(unittest.TestCase):
    def test_inspects_artificial_fixture_without_dropping_any_rows(self):
        config = test_config()
        summary = inspect_csv(
            FIXTURE,
            candidate_keys=config.candidate_keys,
            categorical_fields=config.categorical_fields,
            numeric_fields=("year", "count"),
            expected_values=config.allowed_categories,
            aggregate_indicators=config.aggregate_indicators,
        )
        self.assertEqual(summary["row_count"], 12)
        self.assertEqual(summary["column_count"], 10)
        self.assertEqual(summary["encoding"], "utf-8")
        self.assertEqual(summary["duplicate_full_rows"]["groups"], 1)
        # Raw inspection does not silently normalize the padded synthetic labels.
        self.assertEqual(summary["duplicate_candidate_keys"]["region,unit,year"]["duplicate_groups"], 3)
        self.assertIn("unused_empty", summary["empty_columns"])
        self.assertEqual(summary["potential_aggregate_row_count_at_least"], 1)
        self.assertIn("UnexpectedArtificialCategory", summary["unique_values"]["category"])
        self.assertGreater(summary["invalid_or_unexpected_values"]["category"]["UnexpectedArtificialCategory"], 0)

    def test_reports_csv_parsing_errors_without_silent_recovery(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bad.csv"
            path.write_text('a,b\n1,"unterminated\n', encoding="utf-8")
            summary = inspect_csv(path)
        self.assertTrue(any("CSV parsing/decoding stopped" in issue for issue in summary["parsing_issues"]))

    def test_empty_file_is_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "empty.csv"
            path.write_bytes(b"")
            summary = inspect_csv(path)
        self.assertEqual(summary["row_count"], 0)
        self.assertEqual(summary["column_count"], 0)
        self.assertTrue(summary["parsing_issues"])


if __name__ == "__main__":
    unittest.main()
