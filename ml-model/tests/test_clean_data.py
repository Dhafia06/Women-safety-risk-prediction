import unittest
from dataclasses import replace

from preprocessing.clean_data import clean_records
from preprocessing.config import normalized_header_mapping
from tests.support import load_fixture, test_config


class CleanDataTests(unittest.TestCase):
    def test_cleaning_preserves_every_record_and_quarantines_flagged_rows(self):
        _, records, _ = load_fixture()
        result = clean_records(records, test_config())
        self.assertEqual(result.original_count, 12)
        self.assertEqual(len(result.accepted) + len(result.quarantined), 12)
        self.assertEqual(len(result.quarantined), 4)  # negative, invalid year, and two synthetic RAILWAYS examples
        rail_rows = [item for item in result.quarantined if item["record"]["unit"] == "RAILWAYS"]
        self.assertEqual(len(rail_rows), 2)
        self.assertEqual([item["record"]["count"] for item in rail_rows], [1, 2])
        self.assertTrue(all(any("duplicate_candidate_key" in flag for flag in item["flags"]) for item in rail_rows))
        self.assertEqual(result.flagged_count, 10)
        self.assertTrue(any(change["field"] == "region" for item in result.transformation_audit for change in item["changes"]))
        # The missing count remains blank rather than being imputed to zero.
        blank_record = next(row for row in result.accepted if row["sample_id"] == "S002")
        self.assertEqual(blank_record["count"], "")
        # Artificial parent and child examples remain separate records.
        parent_child = [row["category"] for row in result.accepted if row["category_relation"].startswith("artificial_")]
        self.assertEqual(parent_child, ["ArtificialParent", "ArtificialChild"])
        # Exact full duplicates are flagged, never removed.
        self.assertEqual(sum("duplicate_full_row" in flags for flags in result.flags.values()), 2)

    def test_disabled_quarantine_rule_does_not_route_rows(self):
        _, records, _ = load_fixture()
        config = test_config()
        disabled = replace(config, quarantine_rules=tuple(replace(rule, enabled=False) for rule in config.quarantine_rules))
        result = clean_records(records, disabled)
        self.assertFalse(any(item["record"]["unit"] == "RAILWAYS" for item in result.quarantined))
        self.assertEqual(len(result.accepted) + len(result.quarantined), len(records))

    def test_safe_header_normalization_is_explicit_and_collision_checked(self):
        self.assertEqual(normalized_header_mapping(["Sample ID", "Crime Head"]), {"Sample ID": "sample_id", "Crime Head": "crime_head"})
        with self.assertRaises(ValueError):
            normalized_header_mapping(["A-B", "A B"])


if __name__ == "__main__":
    unittest.main()
