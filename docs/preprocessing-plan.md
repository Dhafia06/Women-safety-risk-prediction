# SafeHer Proposed Dataset Preprocessing Specification

**Status: plan only (updated after Phase 2B follow-up, 2026-11-28).** No steps below have been executed. The five CSVs remain immutable source inputs. The follow-up found strong OGD/NCRB source-family matches for two files and supports only conditional supplementary descriptive use; exact local artifacts/resource license metadata remain to be captured. Secondary compilations remain quarantined and the synthetic file remains test-only. No dataset is cleared for primary predictive analysis. The unresolved RAILWAYS meaning, historical geography, and annual category definitions remain gates for affected analyses.

## 1. Preconditions and source manifest

Before implementation:

1. For each copy, lock the exact source resource/version where available: record source publisher, resource title/URL, source publication period, retrieval date, local SHA-256, record-level license metadata, attribution statement, and observed/derived/synthetic status in a manifest. The OGD IPC 2001–2012 and OGD/NCRB 2013 files may proceed only as appropriately attributed supplementary descriptive sources after their OGD record metadata is archived; matching schema alone is not an exact-byte identity claim.
2. Obtain the NCRB table notes/codebook and determine whether fields count cases registered, incidents, or another unit; resolve category hierarchy and yearly definition changes.
3. Build a source-backed, year-valid geography/reporting-unit crosswalk. Distinguish revenue districts from GRP/Railways/special police units and state/district totals. Preserve splits, merges, and boundary changes as temporal relations; do not map historical aggregates to successor territories by name.
4. Decide the descriptive target and compatible evaluation period before constructing analysis features. Do not create safety labels from crime-count quantiles.
5. Keep original files immutable and verify hashes before/after the preprocessing job.

If any precondition remains unresolved, emit a quality report and quarantine affected records instead of guessing. Eligibility and specific unresolved items are detailed in [`dataset-eligibility-matrix.md`](dataset-eligibility-matrix.md) and the follow-up section of [`dataset-verification-report.md`](dataset-verification-report.md).

## 2. Per-file specification

### `ml-model/dataset/raw/01_District_wise_crimes_committed_IPC_2001_2012.csv`

- **Source role:** potential reference source for annual IPC counts and matching women-crime measures, pending exact OGD artifact verification.
- **Retain initially:** raw state/UT and district labels, `YEAR`, and all 30 named count fields for traceability. Selection of modeling measures happens only after codebook and category hierarchy review.
- **Blank/index-like fields:** retain raw source unchanged; in a processed table, omit the all-empty trailing column with a logged reason. Do not treat its blank header as a data field.
- **Types:** year as integer; numeric category fields as nullable integer/counts only after strict parse and range checks. No silent coercion. Zeros remain zeros unless official notes identify sentinel codes.
- **Aggregates:** mark `DISTRICT=TOTAL`, `DELHI UT TOTAL`, and any other source total/reporting units explicitly. Build district detail and published totals as separate analytical tables. Never include both in a sum.
- **Duplicate:** preserve both rows for `JAMMU & KASHMIR / RAILWAYS / 2010`; set a quality flag, source row ordinal, and quarantine from analyses requiring unique geography until the unit is resolved. Do not average/deduplicate.
- **Geography:** preserve raw strings and add normalized comparison strings. Map only via dated, sourced jurisdiction IDs; a police reporting unit must not be assigned to a revenue-district polygon without documentation.
- **Candidate output:** `processed/ncrb_ipc_district_annual_2001_2012.csv`, with source lineage, source row number, raw labels, geography ID/type, year, crime head/value in long form, and aggregate/duplicate/mapping flags. Keep a wide archival-parity table only if approved.

### `ml-model/dataset/raw/crimes_against_women_2001-2014.csv`

- **Source role:** strongest women-specific district candidate, but exact combined source/version and license are unresolved.
- **Retain initially:** `STATE/UT`, `DISTRICT`, `Year`, all seven category columns, and the original row ordinal in an audit-only field.
- **Blank/index-like field:** establish whether the first numeric column is an export index by comparison to source artifact. Do not use it as an identifier. If confirmed to be an export index, omit it from analysis outputs but preserve it in the immutable source and audit log.
- **Types:** `Year` integer; seven measures strict nonnegative integer counts. Reject/log malformed values rather than silently parsing strings.
- **Aggregates:** flag `TOTAL`, `DELHI UT TOTAL`, `ZZ TOTAL`, `Total District(s)` and other verified totals. Keep published totals separate. Preserve totals in a source-reconstruction table with a `row_type` field.
- **Duplicate:** retain and flag both `JAMMU & KASHMIR / RAILWAYS / 2010` rows; the index and rape values differ. No collapse until source confirms jurisdiction semantics.
- **Geography:** preserve `DELHI` raw label and add a versioned, year-aware crosswalk to compare against `DELHI UT`; standardize case/whitespace only as separate normalized fields. Never normalize historical district changes by string equality alone.
- **Categories:** use official report labels/definitions. Do not map broad kidnapping counts to a women-only field; the measured matching IPC women/girls subcategory is the suitable comparator.
- **Candidate output:** `processed/ncrb_women_district_annual_2001_2014.csv`, long format with geography/reporting unit, year, crime head, count, source ID/version, and quality flags. Build only after validating 2013–2014 provenance.

### `ml-model/dataset/raw/CrimesOnWomenData.csv`

- **Source role:** supplementary state-year panel candidate; local source/license and abbreviations are unresolved.
- **Retain initially:** state, year, and seven category values; retain blank-header index only in audit copy until confirmed as an export index.
- **Types:** year and crime values strict integer-like; parse only after the applicable null/sentinel definitions are known. Preserve zeros.
- **Categories:** retain raw `K&A`, `DD`, `AoW`, `AoM`, `DV`, `WT` names. Add canonical codes only with a source data dictionary; never infer `DV` equals cruelty or `WT` equals importation without verification.
- **Geography:** retain raw `State`; create a dated source crosswalk. Do not merge rows solely on title-case/uppercase normalization if admin identity is not certain.
- **Quality:** check 2001–2021 coverage by state/category, official state/UT roster per year, total rows, and compare each measure with independently verified OGD/NCRB state aggregates.
- **Candidate output:** `processed/ncrb_women_state_annual_2001_2021.csv`, tidy state/year/category/count with source/version and crosswalk status.

### `ml-model/dataset/optional/crcCAW_2013.csv`

- **Source role:** one-year official OGD/NCRB state/UT reference; source metadata strongly matches local shape.
- **Retain:** raw `State/UTs`, `Crime Head`, and numeric `2013`; add explicit year field in a processed representation.
- **Types:** year fixed to 2013; counts strict nonnegative integer. Preserve raw crime head and add mapped code only after glossary confirmation.
- **Aggregates:** keep `Total (State)`, `Total (UTs)`, `Total (All-India)` labeled as aggregate rows. Do not include them when summing state/UT detail. Reconcile aggregate rows to the appropriate state/UT groups only after grouping rules are verified.
- **Candidate output:** `processed/ncrb_women_state_annual_2013.csv`, long-form state/UT/year/crime-head/count plus aggregate flag and provenance.

### `ml-model/dataset/synthetic/india_district_crime_2014_2023_30k.csv`

- **Source role:** synthetic software fixture only until generator/license are documented.
- **Isolation:** never union or join into observed crime data. Keep under a separate synthetic namespace and attach `data_status=synthetic_unverified` to every derived sample.
- **Retain for fixture use:** all 9 columns as input fields. Verify the rate formula and order constraints in tests, but do not treat those checks as proof of realism.
- **No model use:** do not train, tune, select thresholds, or evaluate models using this file. Do not use its district/state labels as an authoritative geography crosswalk.
- **Candidate output if needed:** `processed/synthetic_demo_district_crime_2014_2023.csv`, with an explicit synthetic disclaimer, generator status, and no observed-data merge keys.

## 3. Shared transformations and validation rules

### Missingness and parsing

- Preserve original text and raw rows. Establish a source-specific missing-code map before interpreting blank, dash, `NA`, zero, or other values.
- Report missing counts and percentages for each column, including index-like/empty headers, before and after any approved transformation.
- Parse years as integer and count fields as nonnegative integer. Rate fields may be decimal. Reject infinities, NaN, unexpected types, negative counts, impossible year values, and malformed row lengths to a reject report; never silently coerce.
- Avoid imputing crime counts. A blank is not zero unless source metadata says so. Do not fill years or jurisdictions with zero rows unless the dataset’s reporting coverage supports that interpretation.

### Duplicate and aggregate handling

- Check exact row duplicates and candidate keys at both raw label and canonical geography-ID levels. Preserve source row index and report every collision.
- Do not deduplicate, average, or sum duplicate-key rows automatically. Quarantine unresolved keys, especially the shared 2010 RAILWAYS pair.
- Classify detail, police/reporting units, state totals, UT totals, all-India totals, and other subtotals in a `row_type` field. Keep published aggregate records separate from computed aggregates.
- For each computed total, reconcile to source totals by year/category and publish match/mismatch counts. Avoid adding parent categories to subcategories and avoid adding source totals to detail counts.

### Geography and categories

- Retain raw labels and source-specific normalized labels separately. Trim/collapse whitespace and case-fold for comparisons only; this does not resolve historical identity.
- Use authoritative dated State/UT, district, city, and police-unit identifiers/crosswalks. Record effective dates and source evidence. Keep unresolved labels unassigned instead of approximate geocoding.
- Preserve source crime-head label and define a canonical category code only in a versioned category crosswalk. Record category inclusion changes and mappings as one-to-one, many-to-one, or unresolved. Do not equate crime labels by similarity alone.

### Temporal normalization and feature/target leakage

- Represent reporting year as integer and period frequency as `annual`. Do not invent month/date/time.
- Do not claim a complete panel from continuous year labels alone; make a state/unit × year × category coverage matrix and distinguish structural absence, unreported value, and reported zero using documentation.
- For a future forecast, split chronologically and prevent future totals, derived rates containing the target, and aggregate rows containing the target from entering predictors. Keep synthetic data outside all validation splits.

## 4. Proposed processed schemas

### Observed annual fact table (only after source reconciliation)

| Field | Type | Meaning |
|---|---|---|
| `source_dataset_id` | string | Stable identifier for source/version. |
| `source_file_sha256` | string | Hash of exact input artifact. |
| `source_row_number` | integer | Original one-based data row for traceability. |
| `year` | integer | Annual reporting year. |
| `geo_id` | string/null | Dated official geography/reporting-unit identifier, if verified. |
| `geo_name_raw` | string | Source spelling. |
| `geo_name_normalized` | string | Formatting-only normalization. |
| `geo_level` | enum | `state_ut`, `district`, `city`, `police_unit`, `aggregate`, or `unresolved`. |
| `crime_head_raw` | string | Original source category label. |
| `crime_code` | string/null | Versioned canonical category code, only if verified. |
| `count` | integer/null | Source-reported number with source-specific missing handling. |
| `row_type` | enum | `detail`, `published_total`, `subtotal`, `unresolved`. |
| `quality_flags` | array/string | Duplicate key, unresolved geography, aggregate, parse, and source warnings. |
| `source_url` / `license_id` | string | Provenance and rights lineage. |

Do not combine dissimilar reporting units in one analysis panel merely because their columns fit this schema. Record source-specific measures and mapping confidence.

### Synthetic fixture table

Retain its source columns separately, plus `data_status=synthetic_unverified`, `source_file_sha256`, `generator_status=missing`, and a disclaimer. Do not add a shared observed `source_dataset_id` namespace that makes it look observed.

## 5. Output and reproducibility requirements

Proposed output root is `ml-model/processed/`; no outputs have been created. Use explicit names listed above, versioned schemas/crosswalks, and a generated quality report for every run. Recommended run artifacts:

- input manifest (source URL, publisher, dataset version/date, license, local SHA-256, byte count);
- code/runtime versions and exact command line;
- row counts before/after per source and per filter;
- missing/type/negative/range reports;
- raw and canonical natural-key duplicate reports;
- aggregate reconciliation checks;
- geography/category crosswalk coverage and unresolved labels;
- output hashes and schema version;
- a statement that source files were unchanged.

No dependencies, scripts, outputs, notebooks, or processed files have been created in Phase 2B. Implement this plan only after approval and resolution of the listed blockers.

## 6. Follow-up decision gates

- Keep the duplicate `JAMMU & KASHMIR / RAILWAYS / 2010` source rows intact. Quarantine this key from unique-geography analysis until NCRB/state GRP material determines whether they are distinct units or a source collision.
- Start any approved geography crosswalk with raw label, source/year, and reporting-unit type. Use dated authoritative state/district identifiers and effective intervals; current LGD codes alone do not establish historical boundaries. Keep one-to-many and many-to-one transitions explicit.
- Apply the category crosswalk only as a versioned comparison map. Treat the seven overlapping women-specific measures as locally equivalent only over 2001–2012 for comparison; do not stack the files. Keep category abbreviations unresolved and distinguish IPC from SLL categories. Never sum totals with details or parent categories with subcategories.
- Preserve `CrimesOnWomenData.csv` and the 2001–2014 combined file outside the analysis dataset until their precise upstream artifacts and reuse rights are established. Keep the 2014–2023 synthetic file in a test-only namespace.
- Even after these gates, the approved scope is descriptive annual count analysis, not street-/route-level safety prediction. Geographic location labels and annual counts do not establish route risk or personal risk.
