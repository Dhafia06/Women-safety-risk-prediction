import unittest

from preprocessing.clean_data import clean_records
from preprocessing.validate_data import validate_records
from tests.support import load_fixture, test_config


class ValidateDataTests(unittest.TestCase):
    def test_raw_fixture_reports_errors_warnings_and_preserves_all_rows(self):
        headers, records, _ = load_fixture()
        config = test_config()
        result = validate_records(records, config, headers=headers, original_count=len(records), quarantined_count=0)
        codes = {issue["code"] for issue in result["issues"]}
        self.assertFalse(result["valid"])
        self.assertIn("negative_count", codes)
        self.assertIn("invalid_year", codes)
        self.assertIn("unexpected_categories", codes)
        self.assertIn("duplicate_full_rows", codes)
        self.assertIn("duplicate_candidate_keys", codes)
        self.assertIn("aggregate_detail_mixed", codes)
        self.assertIn("record_count_preserved", codes)
        self.assertEqual(result["counts"]["records_checked"], len(records))

    def test_cleaning_quarantine_and_count_conservation_validate(self):
        headers, records, _ = load_fixture()
        config = test_config()
        cleaned = clean_records(records, config)
        result = validate_records(
            cleaned.accepted,
            config,
            headers=headers,
            original_count=len(records),
            quarantined_count=len(cleaned.quarantined),
        )
        conservation = [issue for issue in result["issues"] if issue["code"] == "record_count_preserved"]
        self.assertEqual(len(conservation), 1)
        self.assertTrue(conservation[0]["severity"] == "INFO")
        self.assertTrue(cleaned.summary()["record_count_preserved"])

    def test_failed_conservation_is_an_error(self):
        headers, records, _ = load_fixture()
        result = validate_records(records[:-1], test_config(), headers=headers, original_count=len(records), quarantined_count=0)
        self.assertFalse(result["valid"])
        self.assertIn("record_count_not_preserved", {issue["code"] for issue in result["issues"]})

    def test_missing_required_column_is_an_error(self):
        config = test_config()
        record = {"region": "ExampleRegion"}
        result = validate_records([record], config, headers=["region"])
        self.assertFalse(result["valid"])
        self.assertIn("required_columns_missing", {issue["code"] for issue in result["issues"]})


if __name__ == "__main__":
    unittest.main()
