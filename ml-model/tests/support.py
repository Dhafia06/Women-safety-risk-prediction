"""Shared helpers whose only data source is the artificial test fixture."""

from pathlib import Path

from preprocessing.config import load_config
from preprocessing.utils import read_csv_rows, rows_to_dicts


FIXTURE = Path(__file__).parent / "fixtures" / "artificial_synthetic_pipeline_cases.csv"
CONFIG_FIXTURE = Path(__file__).parent / "fixtures" / "artificial_synthetic_pipeline_config.json"


def load_fixture():
    headers, rows, encoding = read_csv_rows(FIXTURE)
    return headers, rows_to_dicts(headers, rows), encoding


def test_config():
    return load_config(CONFIG_FIXTURE)
