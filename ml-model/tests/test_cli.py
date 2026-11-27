import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from preprocessing.clean_data import main as clean_main
from preprocessing.generate_report import main as report_main
from preprocessing.inspect_data import main as inspect_main
from preprocessing.validate_data import main as validate_main
from tests.support import CONFIG_FIXTURE, FIXTURE


class CommandLineTests(unittest.TestCase):
    def test_inspect_and_validate_cli_use_explicit_synthetic_paths(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(inspect_main(["--input", str(FIXTURE), "--candidate-key", "region,unit,year"]), 0)
        inspected = json.loads(output.getvalue())
        self.assertEqual(inspected["row_count"], 12)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = validate_main(["--input", str(FIXTURE), "--config", str(CONFIG_FIXTURE)])
        self.assertEqual(result, 1)  # fixture intentionally includes validation errors
        validated = json.loads(output.getvalue())
        self.assertFalse(validated["valid"])

    def test_clean_cli_defaults_to_dry_run_and_write_refuses_overwrite(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = clean_main(["--input", str(FIXTURE), "--config", str(CONFIG_FIXTURE)])
        self.assertEqual(result, 0)
        self.assertTrue(output.getvalue().isascii())
        self.assertTrue(json.loads(output.getvalue())["record_count_preserved"])

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            accepted, quarantine, audit = root / "accepted.csv", root / "quarantine.csv", root / "audit.json"
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = clean_main([
                    "--input", str(FIXTURE), "--config", str(CONFIG_FIXTURE), "--write",
                    "--output", str(accepted), "--quarantine-output", str(quarantine), "--audit-output", str(audit),
                ])
            self.assertEqual(result, 0)
            self.assertTrue(accepted.exists() and quarantine.exists() and audit.exists())
            self.assertEqual(json.loads(audit.read_text(encoding="utf-8"))["preserved_count"], 12)
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                result = clean_main([
                    "--input", str(FIXTURE), "--config", str(CONFIG_FIXTURE), "--write",
                    "--output", str(accepted), "--quarantine-output", str(root / "q2.csv"), "--audit-output", str(root / "a2.json"),
                ])
            self.assertEqual(result, 2)
            self.assertIn("Refusing to overwrite", output.getvalue())

    def test_report_cli_generates_both_formats_from_json_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            inspection = root / "inspection.json"
            validation = root / "validation.json"
            inspection.write_text(json.dumps({"file_name": FIXTURE.name, "file_path": str(FIXTURE), "file_size_bytes": 1, "sha256": "synthetic", "encoding": "utf-8", "row_count": 1, "column_count": 1, "column_names": ["data_status"], "missing_values": {}, "duplicate_full_rows": {}, "duplicate_candidate_keys": {}, "parsing_issues": []}), encoding="utf-8")
            validation.write_text(json.dumps({"valid": True, "severity_counts": {}, "issues": []}), encoding="utf-8")
            json_out, md_out = root / "final.json", root / "final.md"
            self.assertEqual(report_main([
                "--inspection-json", str(inspection), "--validation-json", str(validation),
                "--json-output", str(json_out), "--markdown-output", str(md_out),
            ]), 0)
            self.assertTrue(json_out.exists() and md_out.exists())


if __name__ == "__main__":
    unittest.main()
