# SafeHer Dataset Inspection and Quality Assessment

## 1. Inspection objective and method

This read-only inspection evaluates the datasets currently under `ml-model/dataset/` for descriptive crime visualization and possible future geographic risk estimation. It does not clean, transform, merge, or save any dataset; it does not train a model or access MongoDB or `.env` values.

The five CSV files were read with Python 3.12.6 and the Python standard library (`csv`, `collections`, `pathlib`, and `re`). The checks measured file size, logical rows and columns, headers, simple value types, null-like cells, exact duplicate rows, candidate duplicate natural keys, year coverage, numeric ranges and negative values. The data was not printed as raw records. No Excel files were found, so there were no workbook sheets to inspect. “Missing” below counts blank cells and the literal tokens `NA`, `N/A`, `null`, `none`, and `-`; this is a mechanical scan, not a determination that each such token is semantically missing.

## 2. ML directory inventory

```text
ml-model/
├── dataset/
│   ├── optional/
│   │   └── crcCAW_2013.csv
│   ├── raw/
│   │   ├── 01_District_wise_crimes_committed_IPC_2001_2012.csv
│   │   ├── crimes_against_women_2001-2014.csv
│   │   └── CrimesOnWomenData.csv
│   └── synthetic/
│       └── india_district_crime_2014_2023_30k.csv
├── requirements.txt
└── train_model.py
```

There are no Jupyter notebooks, saved model files, or ML-specific documentation files. `train_model.py` exists but is empty (0 bytes). `requirements.txt` lists `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `jupyter`, and `joblib`.

Python 3.12.6 is available. In the Python environment checked, imports for pandas, NumPy, Matplotlib, Seaborn, scikit-learn, Jupyter, joblib, and openpyxl were all unavailable. No packages were installed. Existing repository documentation includes `docs/incident-reporting.md` and a generic frontend README; neither documents data provenance. No source/metadata manifest was found for these datasets.

## 3. Dataset inventory and measured schemas

There are **5 datasets**, all CSV, totaling **50,886 logical data rows and 67 columns** (row totals are per-file, not deduplicated across files). File sizes are exact filesystem byte counts. All files decoded as UTF-8 with BOM handling (`utf-8-sig`). No decoding errors occurred.

| Relative path | Size | Rows × columns | Measured structure | Years / geography / record type |
|---|---:|---:|---|---|
| `ml-model/dataset/optional/crcCAW_2013.csv` | 20,575 B | 456 × 3 | `State/UTs` (text), `Crime Head` (text), `2013` (numeric) | The year is encoded as the value column name. State/UT label by crime-head count matrix in long form; aggregate rows are present. |
| `ml-model/dataset/raw/01_District_wise_crimes_committed_IPC_2001_2012.csv` | 1,028,098 B | 9,017 × 34 | `STATE/UT`, `DISTRICT`, `YEAR`, 30 numeric crime/count columns, and one blank trailing header/column | Annual district/state-labelled aggregate crime counts, 2001–2012. The crime columns include IPC categories and `TOTAL IPC CRIMES`. |
| `ml-model/dataset/raw/crimes_against_women_2001-2014.csv` | 528,249 B | 10,677 × 11 | Blank header/index column, `STATE/UT`, `DISTRICT`, `Year`, and seven numeric crime-count columns | Annual district/state-labelled counts, 2001–2014, including rape, kidnapping and abduction, dowry deaths, assault, insult, cruelty, and importation of girls. Aggregate-like district labels occur. |
| `ml-model/dataset/raw/CrimesOnWomenData.csv` | 32,551 B | 736 × 10 | Blank header/index column, `State`, `Year`, and seven numeric abbreviated-category columns: `Rape`, `K&A`, `DD`, `AoW`, `AoM`, `DV`, `WT` | State-labelled annual aggregates, 2001–2021. Abbreviations are not defined in repository documentation. |
| `ml-model/dataset/synthetic/india_district_crime_2014_2023_30k.csv` | 1,756,691 B | 30,000 × 9 | `State`, `District`, `Year`, `Crime_Type` (text); `Cases_Reported`, `Chargesheeted`, `Convictions`, `Population`, `Crime_Rate_per_100k` (numeric) | State/district/year/crime-type aggregate-shaped data, 2014–2023. The folder and filename label this file synthetic; no generation method or source is documented. |

### Column names by file

- **`crcCAW_2013.csv`**: `State/UTs`, `Crime Head`, `2013`.
- **`01_District_wise_crimes_committed_IPC_2001_2012.csv`**: `STATE/UT`, `DISTRICT`, `YEAR`, `MURDER`, `ATTEMPT TO MURDER`, `CULPABLE HOMICIDE NOT AMOUNTING TO MURDER`, `RAPE`, `CUSTODIAL RAPE`, `OTHER RAPE`, `KIDNAPPING & ABDUCTION`, `KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS`, `KIDNAPPING AND ABDUCTION OF OTHERS`, `DACOITY`, `PREPARATION AND ASSEMBLY FOR DACOITY`, `ROBBERY`, `BURGLARY`, `THEFT`, `AUTO THEFT`, `OTHER THEFT`, `RIOTS`, `CRIMINAL BREACH OF TRUST`, `CHEATING`, `COUNTERFIETING`, `ARSON`, `HURT/GREVIOUS HURT`, `DOWRY DEATHS`, `ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY`, `INSULT TO MODESTY OF WOMEN`, `CRUELTY BY HUSBAND OR HIS RELATIVES`, `IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES`, `CAUSING DEATH BY NEGLIGENCE`, `OTHER IPC CRIMES`, `TOTAL IPC CRIMES`, and a blank final header.
- **`crimes_against_women_2001-2014.csv`**: blank first header, `STATE/UT`, `DISTRICT`, `Year`, `Rape`, `Kidnapping and Abduction`, `Dowry Deaths`, `Assault on women with intent to outrage her modesty`, `Insult to modesty of Women`, `Cruelty by Husband or his Relatives`, `Importation of Girls`.
- **`CrimesOnWomenData.csv`**: blank first header, `State`, `Year`, `Rape`, `K&A`, `DD`, `AoW`, `AoM`, `DV`, `WT`.
- **`india_district_crime_2014_2023_30k.csv`**: `State`, `District`, `Year`, `Crime_Type`, `Cases_Reported`, `Chargesheeted`, `Convictions`, `Population`, `Crime_Rate_per_100k`.

**Source and intended purpose:** The repository contains no citations, data dictionary, source URLs, license, extraction date, methodology, or generation notes for any CSV. Names suggest crime-statistics topics but do not establish provenance or official status. The three raw-folder files and optional file are aggregated tables, not individual incident records. The synthetic-folder file is also aggregate-shaped, but its values should be treated as synthetic/unverified rather than observed crime evidence. None contains person-level incident narratives.

## 4. Data quality findings

### Missingness, shape, and type findings

| Dataset | Missing cells found | Other measured shape/type findings |
|---|---:|---|
| `crcCAW_2013.csv` | 0 / 1,368 (0%) | All 456 rows have the expected 3 fields. Two text and one numeric column. |
| `01_District_wise_crimes_committed_IPC_2001_2012.csv` | 9,017 / 306,578 (2.94%) | The 9,017 missing cells are all in the blank final column. Thus all 33 named fields are populated. Header has an extra delimiter/trailing empty column. |
| `crimes_against_women_2001-2014.csv` | 0 / 117,447 (0%) | First header is blank and acts like an index field; its values are numeric-looking. Other named fields parse consistently as text identifiers, year, and numeric counts. |
| `CrimesOnWomenData.csv` | 0 / 7,360 (0%) | First header is blank and acts like an index field; remaining columns parse consistently as year, text state labels, and numeric values. |
| `india_district_crime_2014_2023_30k.csv` | 0 / 270,000 (0%) | Four text and five numeric columns; all 30,000 rows have the expected 9 fields. |

No malformed row widths were found. No exact duplicate full rows were found in any file. A candidate natural key (geography plus year, and crime type where present) found **one duplicate key group** in each district file: `01_District...` has two rows sharing a state/district/year key that differ in 13 columns; `crimes_against_women...` has a duplicated state/district/year key whose rows differ in 2 columns. The values are not reproduced here. These are confirmed key collisions, but whether they are erroneous, subtotal/detail distinctions, or source conventions requires investigating the affected rows and source definitions before deciding whether to remove or aggregate anything.

No negative values were found in columns that were consistently numeric in each file. Annual year values are four-digit numeric values. There are no exact incident date or time fields to validate. The 2013 optional file expresses its period in a column header, not a row-level period field. The IPC file has a wholly blank trailing column. Two women-crime files have blank first header/index columns; these should be investigated as possible exported row indices, not assumed to be meaningful identifiers.

### Aggregates, totals, categories, and outliers

- `crcCAW_2013.csv` contains 36 labels across `Total (State)`, `Total (UTs)`, and `Total (All-India)` (12 rows per label). These are aggregate rows that must not be summed with constituent state/UT rows without checking the table’s design.
- The IPC district file has district labels `TOTAL` (408 rows) and `DELHI UT TOTAL` (12 rows). The women-specific district file has `TOTAL` (408), `DELHI UT TOTAL` (12), `ZZ TOTAL` (35), and `Total District(s)` (36). These labels strongly indicate subtotal/aggregate records mixed with district-labelled records; their semantics need source verification. Blind aggregation risks double counting.
- The IPC file has a total column and component categories; some categories appear hierarchically related (for example, rape subcategories alongside rape, and theft subcategories alongside theft). Summing all category columns could double count. The repository does not document category definitions.
- `CrimesOnWomenData.csv` has 70 distinct state strings across its 736 rows, much higher than a current stable state/UT roster. This is a measured label cardinality, not a verified count of official jurisdictions. It may include total labels, name variants, or inconsistencies; inspect label frequencies and source metadata before standardizing.
- The earlier district files report 35 distinct state/UT strings (IPC) and 72 (women-only), while the synthetic file contains only 12 states and 300 district strings. These counts do not demonstrate equivalent geographic coverage.
- The synthetic file has minimum and maximum values: cases 20–1,200; chargesheeted 13–1,135; convictions 5–835; population 810,709–6,937,751; rate 0.31–144.44 per 100k. These ranges are not enough to determine outliers or plausibility without source/generation methodology and row context. Its rate equals `Cases_Reported / Population × 100,000` rounded to two decimals in all 30,000 rows, and chargesheeted ≤ cases and convictions ≤ chargesheeted in all rows. This verifies internal arithmetic/order consistency only, not real-world validity.

### Geography/category consistency and privacy

Column labels differ in case, punctuation, abbreviations, wording, and granularity (`State/UTs`, `STATE/UT`, `State`; district fields exist only in some files). The two index-like columns need interpretation. The synthetic categories include 10 text labels; the raw datasets use many distinct columns and category definitions. No geography crosswalk or crime-category dictionary exists, so name normalization and semantic alignment are not yet verified.

No personal names, phone numbers, street addresses, coordinates, police-station fields, or person-level identifiers are present in the inspected schemas. The datasets appear aggregate, reducing direct individual-identification exposure. Aggregated small counts can still be sensitive in very small areas, and the user-generated incident system is separate and may contain sensitive descriptions; do not combine it with these files without a privacy review and data minimization.

## 5. Geographic analysis

| Capability | Classification | Evidence and limits |
|---|---|---|
| State-level estimation/visualization | **Partially supported** | State/UT labels and yearly/category counts exist. Labels and reporting methods vary, aggregate rows are mixed in, and no source metadata or boundary crosswalk is provided. Descriptive state-level historical displays may be possible after verification. |
| District-level estimation/visualization | **Partially supported** | Two raw files include state and district labels with annual counts; the synthetic file has district labels and population. The natural-key collisions, subtotal rows, jurisdiction/name changes, synthetic provenance, and absent boundary identifiers constrain reliability. No district coordinates or boundary geometry are supplied. |
| City-level estimation | **Not supported** | No explicit city field; district labels are not city identifiers. |
| Street-level estimation | **Not supported** | No address, coordinates, police station, or incident-level record fields. District counts cannot justify street-level predictions. |
| Map-based visualization | **Partially supported** | State/district labels can support a future join to an independently sourced/approved boundary or geocoding reference, but no geometries, coordinates, codes, or crosswalks are included here. |
| Route-level risk comparison | **Not supported** | No streets, route segments, coordinates, incident locations, or time-of-day data. These datasets cannot characterize route-specific safety. |

The finest geographic resolution in the files is **district label**, which is not equivalent to a stable geographic identifier or geospatial boundary. State and district name labels alone do not prove a reliable join to maps.

## 6. Temporal analysis

| Dataset | Earliest–latest annual period | Gaps in observed year labels |
|---|---|---|
| `crcCAW_2013.csv` | 2013 (header) | Not applicable; one period encoded as a column. |
| `01_District_wise_crimes_committed_IPC_2001_2012.csv` | 2001–2012 | None within the year values present. |
| `crimes_against_women_2001-2014.csv` | 2001–2014 | None within the year values present. |
| `CrimesOnWomenData.csv` | 2001–2021 | None within the year values present. |
| `india_district_crime_2014_2023_30k.csv` | 2014–2023 | None within the year values present. |

These are annual aggregates, not event dates. Annual year values being gap-free does **not** prove every state/district/category has complete observations in every year. No monthly, daily, hourly, or incident-time data exists. The finest time resolution is annual. Historical descriptive trends are potentially possible after checking coverage and definitions. Forecasting cannot be justified from the current inspection alone: the series length, synthetic status, reporting changes, target definition, and validation scheme need resolution. Time-of-day risk estimation is unsupported.

## 7. Dataset compatibility and possible integration

### Potentially compatible, subject to verification

- `01_District_wise_crimes_committed_IPC_2001_2012.csv` and `crimes_against_women_2001-2014.csv` share state/UT, district, and annual year keys and overlap for 2001–2012. Category names overlap conceptually, but the women-only file is likely a subset/re-expression of related crime reporting. Before joining, verify provenance, overlapping measures, duplicate keys, subtotal rows, definition differences, and whether counts would be duplicated.
- `CrimesOnWomenData.csv` can potentially be compared to or derived from state-level aggregates in the district women file for overlapping years 2001–2014. Candidate key is standardized state/UT plus year; abbreviated categories need an authoritative dictionary. The index column and state labels need verification. Do not append these as new observations without establishing whether they are independent or a re-aggregation.
- `crcCAW_2013.csv` may be comparable to state-level crime-head statistics for 2013. It uses one year as a numeric column, has explicit total rows, and may use different category definitions. A reshape and crosswalk would be required only after source/methodology verification.

### Keep separate for now

- `india_district_crime_2014_2023_30k.csv` should remain separate from observed historical sources because its repository path labels it synthetic and gives no generation details. It can be used to exercise code pipelines or UI using clearly labelled synthetic data, but not as factual crime evidence or as validation truth.

Potential keys are state/UT + district + year for district aggregates and state/UT + year for state aggregates, with crime category added when represented as a row. Names alone are weak keys because jurisdictions and spellings change. Joining statewide totals to district rows, or summing subtotal and constituent rows, risks double counting. Combining overlapping source files also risks duplicating the same reported counts. No merge has been performed.

## 8. ML feasibility assessment

The observed-source files could support descriptive annual counts by reported category and geography once the source, aggregates, and label crosswalks are verified. A carefully defined future target might be a next-year count for a specified reported category and geographic unit, or an annual count/rate baseline. This is a forecasting target proposal, not a safety label. A statistical baseline and temporal holdout should be established before considering more complex supervised models.

At present, meaningful supervised learning is **not established**:

- No explicit target or operational definition of “risk” exists. Reported counts do not equate to personal safety or probability of victimization.
- There are annual aggregates and possible population only in the synthetic file. The observed datasets lack population/exposure denominators, so observed crime rates normalized by residents cannot be calculated from these files alone. Population is a limited proxy for exposure and does not capture visitors, travel volumes, or reporting rates.
- The synthetic file's population and computed rate can illustrate arithmetic but must not be treated as real labels or validation data.
- Validation must respect time (train on earlier years, evaluate later years), preserve geographic/group boundaries as appropriate, and compare against simple baselines. Random row splits would leak shared geography/year/category structure and overstate performance.
- Category totals and subcategories may overlap, aggregate rows can leak sums of target counts, and derived rate fields can leak a count target if used as an input. Avoid including totals or features computed from the prediction period.
- Crime reporting is affected by underreporting, law/enforcement practices, changing definitions, and administrative boundaries. The current files include no covariates for infrastructure, lighting, footfall, transit, weather, time of day, or safety-service availability.

**Feasibility judgment:** State/district-level descriptive risk indicators may be explored cautiously after validation and explicit caveats. Predictive location risk is not yet responsibly supportable from the inspected evidence. Route-level and street-level prediction is not supported by these datasets.

## 9. Dataset-specific preprocessing plan (not executed)

### `01_District_wise_crimes_committed_IPC_2001_2012.csv`

- Retain state/UT, district, year, and selected documented category counts. Investigate every category definition and the `TOTAL IPC CRIMES` relationship before selecting count features.
- Investigate/remove the blank trailing column only after confirming it contains no data (measured all blank); inspect duplicate state/district/year group and total-like district labels.
- Parse year and count fields as integer-like values; preserve zero as a real reported value unless source notes say otherwise.
- Verify official source, state/district boundary changes, label variants, subtotal rows, and category hierarchy. Do not sum category columns indiscriminately.
- Candidate processed format: CSV or Parquet with an explicit schema and source/version metadata; keep totals separately marked if their role is established.

### `crimes_against_women_2001-2014.csv`

- Retain state/UT, district, year, and category counts after reviewing the seven category definitions.
- Investigate the blank header/index field, the duplicated state/district/year key, and labels `TOTAL`, `DELHI UT TOTAL`, `ZZ TOTAL`, `Total District(s)` before any removal or aggregation.
- Parse year and counts as integer-like values; standardize state/district strings via a sourced jurisdiction crosswalk, not ad hoc text replacement.
- Determine overlap with the IPC dataset and whether annual counts are the same source/reported measure. Keep separate until verified.
- Candidate processed format: tidy long table (`state`, `district`, `year`, `category`, `count`) plus provenance fields, if source semantics permit.

### `CrimesOnWomenData.csv`

- Retain state, year, and measure columns only after documenting abbreviations (`K&A`, `DD`, `AoW`, `AoM`, `DV`, `WT`) and source definitions.
- Investigate the blank index column and 70 distinct state labels; classify total rows and jurisdiction variants from metadata before mapping.
- Convert year/counts to integer-like types, reshape category columns to long form only with a verified category map, and compare against district-level aggregation for overlapping years.
- Do not combine with other state totals until source independence and total-row semantics are confirmed.
- Candidate processed format: tidy annual state/category/count table with crosswalk version and source provenance.

### `crcCAW_2013.csv`

- Retain state/UT, crime head, and numeric 2013 count after verifying whether `Crime Head` terminology and legal definitions align with other sources.
- Explicitly classify the 36 total rows. Reshape the year-valued column into an explicit year field only in a later, approved preprocessing stage.
- Investigate spelling variants in category labels and state/UT naming with authoritative source metadata; do not silently map.
- Candidate processed format: tidy state/UT/year/category/count table with total-row flag and provenance.

### `india_district_crime_2014_2023_30k.csv`

- Keep separate and mark every downstream use as synthetic. Obtain generation method, source basis, and intended semantics before using it beyond software demonstrations.
- Retain geography, year, crime type, reported cases, chargesheeted, convictions, population, and rate only if each field's definition is documented.
- Recompute derived rate in a controlled future pipeline and verify formula; the current values are arithmetically consistent. Avoid using both count and derived rate as independent predictors of the same target.
- Confirm whether population is constant across years by district and whether synthetic rows imply repeated geography/category combinations; validate against intended generator constraints.
- Candidate processed format: separate synthetic CSV/Parquet with explicit `synthetic=true` provenance and schema; never merge into observed data by default.

### Cross-dataset sequence

1. Obtain source citations, licenses, codebooks, collection dates, and definitions for every file.
2. Establish an authoritative state/district identifier crosswalk by year and classify aggregate/subtotal rows.
3. Resolve the two duplicate natural-key groups and determine exact overlap among raw files.
4. Document category definitions/hierarchies and reporting-period compatibility.
5. Build separate validated tidy tables for state annual, district annual, and synthetic demonstration data.
6. Only after explicit overlap checks, create a versioned integration table and retain source lineage; verify no double counting and publish row-count reconciliations.

No preprocessing steps above have been performed.

## 10. Limitations, privacy, and next steps

- Provenance, licensing, collection methods, and definitions are undocumented in the repository. Filenames are not proof of source.
- Two district tables contain possible aggregate rows and one natural-key collision each. Category hierarchies and subtotal semantics may create double counting.
- State/district labels are not stable geographic IDs, and administrative changes span the observed years.
- No observed-source population denominator, coordinates, boundaries, street network, police-station field, incident timestamp, or time-of-day information is present.
- Synthetic data has no documented generator and cannot substantiate real-world risk or model accuracy.
- Aggregate data avoids direct personal records in these files, but small-cell disclosure and broader sensitive-data linkage still require review. The separate user-submitted incidents should not be joined casually.

Recommended next steps: obtain and record dataset provenance/license/data dictionaries; investigate the flagged duplicate keys and aggregate labels using a controlled review; decide a narrowly defined descriptive target at state or district annual level; source a versioned geographic crosswalk and (if rate estimation is intended) compatible population denominators; then request approval for a separate preprocessing phase. Do not begin street/route claims from this dataset collection.

## 11. Commands and verification

Commands/checks executed in read-only mode:

- `Get-ChildItem -Force -Recurse ml-model` and documentation inventory.
- `python --version` → Python 3.12.6.
- `python -c "import importlib.util ..."` for pandas, NumPy, Matplotlib, Seaborn, scikit-learn, Jupyter, joblib, and openpyxl → all unavailable in the checked environment.
- Inline Python standard-library CSV scans for dimensions, headers, inferred cell types, missing markers, full-row duplicates, candidate geographic/year keys, duplicate natural keys, year ranges/gaps, numeric negatives, ranges, synthetic consistency checks, and category/aggregate-like labels.

No package installation, dataset write, preprocessing, merge, model training, database access, or commit/push occurred. The only file created for this phase is `docs/dataset-inspection-report.md`.
