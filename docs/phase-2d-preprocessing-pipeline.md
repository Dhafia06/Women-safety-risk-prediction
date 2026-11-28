# SafeHer Phase 2D: Preprocessing Pipeline Development

**Status:** Pipeline implementation and synthetic testing only. This phase does not authorize processing any research dataset. The OGD/NCRB license review remains unresolved, and no supervisor approval for actual research-data processing has been recorded.

## Architecture

The Python package is `ml-model/preprocessing/`. Modules accept explicit input paths and caller-supplied configuration; there is no automatic discovery or activated configuration for the research CSVs.

```text
explicit CSV path + explicit JSON config
                  │
       ┌──────────┴───────────┐
       ▼                      ▼
 inspect_data             validate_data
       │                      │
       └──────────┬───────────┘
                  ▼
              clean_data
      accepted rows + quarantine
                  │
                  ▼
           generate_report
        JSON + readable Markdown
```

### Directory structure

```text
ml-model/
├── dataset/
│   ├── raw/                 # Existing source files; unchanged
│   ├── optional/            # Existing optional source; unchanged
│   ├── synthetic/           # Existing synthetic project file; not used here
│   ├── interim/             # Empty; future derived outputs only
│   ├── processed/           # Empty; future derived outputs only
│   └── quarantined/         # Empty; future review outputs only
├── notebooks/               # Empty
├── preprocessing/
│   ├── __init__.py
│   ├── config.py
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── validate_data.py
│   ├── generate_report.py
│   └── utils.py
├── reports/                 # Empty; reports are generated only on explicit command
├── source-verification/
│   └── official-downloads/  # Existing user downloads; ignored by Git
├── tests/
│   ├── fixtures/
│   │   ├── artificial_synthetic_pipeline_cases.csv
│   │   └── artificial_synthetic_pipeline_config.json
│   ├── support.py
│   ├── test_cli.py
│   ├── test_clean_data.py
│   ├── test_generate_report.py
│   ├── test_inspect_data.py
│   └── test_validate_data.py
├── requirements.txt         # Existing environment declaration; unchanged in Phase 2D
└── train_model.py           # Existing file; unchanged
```

Existing `raw/`, `optional/`, `synthetic/`, `.venv/`, `requirements.txt`, `train_model.py`, and official-download contents were not moved or overwritten. The official-download directory is excluded by the existing `.gitignore` rule.

## Module responsibilities

### `preprocessing/config.py`

- Defines immutable `DatasetConfig` and exact-match `QuarantineRule` configuration models.
- Loads explicit JSON configuration; contains no real dataset schema, geography mapping, category mapping, or enabled production rules.
- Provides opt-in safe header-name normalization with a mapping back to original labels and collision rejection.

### `preprocessing/inspect_data.py`

- Read-only inspection of one explicitly supplied CSV.
- Reports file metadata and SHA-256, row/column counts, raw column names, inferred data types, blank-cell counts, exact duplicate rows, explicitly configured candidate-key duplicates, selected unique values, numeric ranges, unexpected values, potential total-like rows, empty columns, row-width issues, encoding and parse/decode issues.
- Does not remove records. Total-like detection is lexical and advisory; it is not a deletion rule.
- Counts only blank strings as missing. Tokens such as `NA`, `-`, and `null` stay literal unless a future approved source-specific config says otherwise.

### `preprocessing/clean_data.py`

- Applies only configured outer-whitespace trims, strict type conversions, optional header mapping, and enabled exact-match quarantine rules.
- Keeps accepted and quarantined rows separate; every input row must appear in one of those outputs. The quarantine sidecar includes source row number, reasons, and quality flags.
- Does not impute missing values, delete duplicates, average or merge rows, merge geographies, sum categories, or remove totals.
- Duplicate full rows and candidate-key repeats are flagged after explicitly configured transformations. They remain present.
- Defaults to dry-run. Writing requires `--write` plus explicit accepted, quarantine, and audit destinations. Destinations must be new files; existing files are refused.

### `preprocessing/validate_data.py`

- Returns structured `ERROR`, `WARNING`, and `INFO` results for required/expected fields, numeric constraints, missing values, duplicate full rows/keys, year values/ranges, category vocabularies, aggregate/detail coexistence, row-schema consistency, and input/accepted/quarantine count conservation.
- Validation never repairs a record. Duplicate keys are warnings unless another explicitly defined constraint says otherwise; there is no generic assumption that repeated keys are errors.

### `preprocessing/generate_report.py`

- Combines inspection, validation, optional cleaning audit, configuration, execution time, and software information.
- Writes machine-readable JSON and readable Markdown only to explicit new output paths; it refuses overwrites.
- The report includes input identity and hash, record counts, missing/duplicate statistics, validation issues, transformations, flags, errors, and warnings.

### `preprocessing/utils.py`

- Implements streaming SHA-256, BOM/UTF-8 detection with an explicit cp1252 fallback note, strict CSV parsing, safe record conversion, deterministic JSON serialization, and exclusive-create writers.
- Malformed row widths are reported or rejected for record operations; they are never silently padded into clean output.

## Synthetic test strategy

All automated tests use `tests/fixtures/artificial_synthetic_pipeline_cases.csv`, an artificial fixture whose rows carry `ARTIFICIAL_TEST_ONLY`. Its field names and values are invented solely as test scaffolding and do not represent NCRB columns, crime statistics, legal categories, or real locations. The fixture config is similarly artificial and is not a production data config.

Scenarios exercised:

1. Valid artificial annual unit records.
2. Missing count retained as blank and reported.
3. Negative count validation error and cleaning quarantine.
4. Duplicate full rows detected, flagged, and retained.
5. Duplicate region/unit/year keys detected independently from exact duplicates.
6. A `TOTAL`-label example is flagged as potentially aggregate; not removed.
7. Artificial parent/child category labels remain separate; no totals are calculated.
8. Unexpected artificial category is reported/flagged.
9. Two artificial `RAILWAYS` rows with different counts are both quarantined, with no deletion or combining.
10. Empty column is reported.
11. Invalid year is reported and quarantined by configured validation/conversion policy.
12. Count conservation checks ensure accepted plus quarantined equals original rows.

Temporary malformed/empty CSVs and temporary report outputs used by tests are created under the OS temporary directory and removed by the test harness. No tests read any file under `ml-model/dataset/` or `source-verification/official-downloads/`.

## Data protection and unresolved decisions

- Actual research datasets were not supplied to inspection, validation, cleaning, or report commands during Phase 2D.
- The synthetic 2014–2023 project CSV was not used as observed evidence or as a test fixture.
- The unresolved J&K / RAILWAYS issue is represented only by an artificial fixture scenario. No real record, district mapping, or NCRB category mapping is configured.
- No geography/crosswalk or IPC/SLL/category aggregation rules are activated.
- Official downloads remain outside Git tracking while license questions remain unresolved.
- This pipeline does not authorize processing or redistribution. A future phase requires resource-level license review, supervisor/user approval, source-specific config review, and a narrowly scoped dry run.

## Commands

Open PowerShell in `ml-model/`. Use the existing virtual environment; packages were not installed for this phase.

### Run tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Inspect an explicitly supplied CSV

```powershell
.\.venv\Scripts\python.exe -m preprocessing.inspect_data `
  --input .\tests\fixtures\artificial_synthetic_pipeline_cases.csv `
  --candidate-key region,unit,year `
  --categorical-field category `
  --numeric-field year --numeric-field count `
  --output-json .\reports\artificial-inspection.json
```

### Validate an explicitly supplied CSV

```powershell
.\.venv\Scripts\python.exe -m preprocessing.validate_data `
  --input .\tests\fixtures\artificial_synthetic_pipeline_cases.csv `
  --config .\tests\fixtures\artificial_synthetic_pipeline_config.json `
  --output-json .\reports\artificial-validation.json
```

The fixture intentionally contains invalid values, so validation writes a report and returns exit code `1` when validation issues are present. Exit code `2` indicates an input/config/output error.

### Dry-run cleaning (default)

```powershell
.\.venv\Scripts\python.exe -m preprocessing.clean_data `
  --input .\tests\fixtures\artificial_synthetic_pipeline_cases.csv `
  --config .\tests\fixtures\artificial_synthetic_pipeline_config.json
```

### Controlled synthetic output

Only after reviewing the dry-run summary, output can be written to new destinations:

```powershell
.\.venv\Scripts\python.exe -m preprocessing.clean_data `
  --input .\tests\fixtures\artificial_synthetic_pipeline_cases.csv `
  --config .\tests\fixtures\artificial_synthetic_pipeline_config.json `
  --write `
  --output .\dataset\interim\artificial-accepted.csv `
  --quarantine-output .\dataset\quarantined\artificial-review.csv `
  --audit-output .\reports\artificial-clean-audit.json
```

Existing files are never overwritten. Choose new output names for each run. Do not substitute an actual research CSV for the fixture during this phase.

### Generate JSON and Markdown reports

```powershell
.\.venv\Scripts\python.exe -m preprocessing.generate_report `
  --inspection-json .\reports\artificial-inspection.json `
  --validation-json .\reports\artificial-validation.json `
  --cleaning-json .\reports\artificial-clean-audit.json `
  --config-json .\tests\fixtures\artificial_synthetic_pipeline_config.json `
  --json-output .\reports\artificial-run.json `
  --markdown-output .\reports\artificial-run.md
```

All output arguments must be new paths. This phase did not run commands that write reports under `ml-model/reports/`; report-generation tests use temporary paths.

## Verification performed

- Python used: existing `ml-model/.venv`, Python 3.12.6.
- Test runner: built-in `unittest`; no package installation.
- Result: **16 tests passed**. They cover inspection, cleaning, validation, quarantine, preservation, report generation, deterministic output, CLI behavior, and no-overwrite errors.
- Test command: `python -m unittest discover -s tests -v` from `ml-model/`.
- All test data was artificial or created in temporary memory/directories. No model was trained and no network, MongoDB, `.env`, research CSV, or official download was accessed by pipeline tests.

## Known limitations and future activation requirements

- No real dataset config exists. Required fields, missing sentinels, category definitions, legal mappings, geographic IDs, aggregate classification, and exclusion policies must not be inferred from this package.
- Inspector duplicate and row-value summaries use memory proportional to the input size; very large files may need a future streaming/disk-backed implementation.
- Encoding detection can identify common BOMs and valid UTF-8. The cp1252 path is heuristic and reported as such; source owners should confirm encodings if it occurs.
- Lexical “total” detection can produce false positives and is advisory only.
- Multiple independent output files are protected against existing paths but a hardware/process failure between writes could leave a partial output set. Verify output counts and hashes before use.
- Actual preprocessing and EDA remain blocked until license, provenance, categories, geography, RAILWAYS semantics, exact config, and approval gates are satisfied.
