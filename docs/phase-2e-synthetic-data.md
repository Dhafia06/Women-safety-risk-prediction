# SafeHer Phase 2E: Synthetic Data Generation and Preprocessing

**Status: complete for software development and testing only.** The actual research datasets remain blocked pending resource-level license clarification. They and the official downloads were not used in this phase.

## Purpose and limits

Artificial data lets the team exercise the generator, inspection, cleaning, validation, quarantine, and report-writing paths without reading or deriving from research data. It is not a substitute for source-verified crime statistics.

Generated state, district, reporting-unit, and crime-category labels are invented identifiers prefixed with `SYNTH_`. Every row contains `Dataset_Label=SYNTHETIC_ARTIFICIAL_ONLY_NOT_REAL_STATISTICS`. Counts come from a seeded pseudorandom generator and are arbitrary software-test values. No distribution or value represents Indian crime patterns, real locations, or observed incidents. These files cannot support EDA of actual crime, predictive accuracy claims, safety recommendations, or production readiness.

The existing `ml-model/dataset/synthetic/india_district_crime_2014_2023_30k.csv` was not read or modified. The new files have separate names and are clearly labelled.

## Generator

Implementation: `ml-model/data_generation/generate_synthetic_data.py`  
Configuration: `ml-model/data_generation/synthetic_pipeline_config.json`  
Default seed: `20261128`

The main file contains **240** annual records: five artificial years, four invented state labels, four invented districts per label, and three synthetic categories. The separate **12-row** scenario file contains valid and missing-value records, a repeated full record, invalid and negative counts, an aggregate-like district label, multiple reporting units, repeated ambiguous geography/year/category keys, and an unexpected synthetic category.

## Run the generator

From PowerShell, start in `ml-model/` and use the existing virtual environment:

```powershell
.\.venv\Scripts\python.exe -m data_generation.generate_synthetic_data
```

The command creates these new files and refuses to overwrite them:

- `dataset/synthetic/synthetic_crime_data.csv`
- `dataset/synthetic/synthetic_test_cases.csv`

To make another run, supply new output filenames and (optionally) another seed:

```powershell
.\.venv\Scripts\python.exe -m data_generation.generate_synthetic_data `
  --seed 20261128 `
  --dataset-output dataset/synthetic/synthetic_crime_data_run2.csv `
  --test-cases-output dataset/synthetic/synthetic_test_cases_run2.csv
```

## Run the preprocessing pipeline

The commands below run from `ml-model/`. All output paths must be new because the pipeline refuses overwrites.

```powershell
.\.venv\Scripts\python.exe -m preprocessing.inspect_data `
  --input dataset/synthetic/synthetic_crime_data.csv `
  --candidate-key Year,State,District,Crime_Category `
  --categorical-field Crime_Category --categorical-field Reporting_Unit `
  --numeric-field Year --numeric-field Crime_Count `
  --output-json reports/synthetic/pipeline-run/main-inspection.json

.\.venv\Scripts\python.exe -m preprocessing.clean_data `
  --input dataset/synthetic/synthetic_crime_data.csv `
  --config data_generation/synthetic_pipeline_config.json --write `
  --output dataset/processed/synthetic/synthetic_crime_data_processed.csv `
  --quarantine-output dataset/quarantined/synthetic/synthetic_crime_data_quarantined.csv `
  --audit-output reports/synthetic/pipeline-run/main-cleaning-audit.json

.\.venv\Scripts\python.exe -m preprocessing.validate_data `
  --input dataset/processed/synthetic/synthetic_crime_data_processed.csv `
  --config data_generation/synthetic_pipeline_config.json `
  --output-json reports/synthetic/pipeline-run/main-validation.json

.\.venv\Scripts\python.exe -m preprocessing.generate_report `
  --inspection-json reports/synthetic/pipeline-run/main-inspection.json `
  --validation-json reports/synthetic/pipeline-run/main-validation.json `
  --cleaning-json reports/synthetic/pipeline-run/main-cleaning-audit.json `
  --config-json data_generation/synthetic_pipeline_config.json `
  --json-output reports/synthetic/synthetic_quality_report.json `
  --markdown-output reports/synthetic/synthetic_quality_report.md
```

The scenario CSV is also covered by integration tests that call the same existing modules. Its raw validation is expected to return exit code `1` because invalid and negative counts are deliberately present. Cleaning quarantines those two rows; blank count, duplicate rows, aggregate-like rows, ambiguous keys, and unexpected category examples remain preserved and are reported/flagged according to the explicit config. No row is silently deleted, imputed, merged, or averaged.

Run all tests from `ml-model/`:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Results from this run

| Input | Original | Accepted | Quarantined | Flagged | Validation |
|---|---:|---:|---:|---:|---|
| `synthetic_crime_data.csv` | 240 | 240 | 0 | 0 | Valid; no warnings/errors |
| `synthetic_test_cases.csv` | 12 | 10 | 2 | 9 | Intentionally invalid raw input; expected errors/warnings |

For the main generated file, the input SHA-256 is `4949B382C0208546A6969602C8FF780D3357CC59E1909A6C584427102F207020`. Its 240 output records are preserved; the quarantine CSV contains only its header. The 12 scenario records are partitioned as 10 accepted plus 2 quarantined. The missing count remains blank; duplicate and ambiguous keys are retained; the aggregate-like and unexpected-category records are not deleted.

The full suite reports **19 tests passed**, including the 16 previous pipeline tests and three generator/integration tests. The suite uses the existing virtual environment; no packages were installed.

## Outputs

- Generated inputs: `ml-model/dataset/synthetic/synthetic_crime_data.csv` and `synthetic_test_cases.csv`.
- Main processed output and audit: `ml-model/dataset/processed/synthetic/` and `ml-model/reports/synthetic/pipeline-run/`.
- Quarantine outputs: `ml-model/dataset/quarantined/synthetic/`.
- Requested quality summary: `ml-model/reports/synthetic/synthetic_quality_report.json` and `.md`.

## Distinguishing synthetic from research data

Use the `Dataset_Label` value and the `SYNTH_` identifier prefixes. Keep these files in the existing `dataset/synthetic/` subtree, and do not cite them as NCRB/OGD data or mix them with research datasets. A successful pipeline validation means only that these artificial records satisfy this software configuration; it says nothing about the accuracy, fairness, safety, or real-world usefulness of a model.

## Limitations

- The generator has no empirical basis and its random count range is arbitrary.
- The scenario rows are deliberately malformed/ambiguous and are not intended as a representative dataset.
- The test config's category vocabulary and key choices are software fixtures, not an endorsed crime taxonomy or geography model.
- The current quality report describes the valid 240-row main file; scenario-specific validation evidence is in `reports/synthetic/pipeline-run/scenarios-validation.json` and the automated integration test.
- Real-data preprocessing remains blocked until item-level license applicability and source attribution are verified. No EDA, feature engineering, model training, production model, or real-world prediction was performed.
