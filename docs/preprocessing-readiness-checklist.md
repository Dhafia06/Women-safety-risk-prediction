# SafeHer Preprocessing Readiness Checklist

**Review date:** 2026-11-28  
**Decision:** No source dataset is authorized for preprocessing by this readiness review. Two OGD/NCRB candidates have strong source-family/structural evidence but remain blocked until record-level license and exact artifact lineage are verified. No data has been cleaned, transformed, or merged.

### Phase 2E addendum

The supervisor/user authorization for the narrowly scoped Phase 2E work has now been received. This satisfies the project approval condition for the attempted phase, but it does not replace publisher licensing conditions. The resource-level license metadata for both OGD/NCRB candidates remains unresolved; the OGD Terms of Use direct users to each individual record's `license` metadata. Therefore neither candidate was read by the preprocessing pipeline, and the dataset readiness decisions below remain **Blocked pending verification**. The synthetic-only pipeline suite passed 16 tests. See [Phase 2E dataset preprocessing](phase-2e-dataset-preprocessing.md).

## Dataset readiness decisions

| Dataset | Decision | Reason and permitted scope at this checkpoint |
|---|---|---|
| `ml-model/dataset/raw/01_District_wise_crimes_committed_IPC_2001_2012.csv` | **Blocked pending verification** | Official download `dstrIPC_1.csv` is identified by expected schema/period and matches all 9,017 existing records as an unordered multiset over the 33 named fields. It is not byte-identical: local file has an empty 34th field and different row ordering. Resource-level license applicability remains unverified. RAILWAYS/special-unit and aggregate exclusions remain mandatory. |
| `ml-model/dataset/optional/crcCAW_2013.csv` | **Blocked pending verification** | Official download `crcCAW_2013.csv` matches the existing local file byte-for-byte (SHA-256, size, schema, rows). The resource-level license applicability to this file is not conclusively captured. State/UT totals and SLL/IPC categories require explicit treatment. |
| `ml-model/dataset/raw/crimes_against_women_2001-2014.csv` | **Blocked pending verification** | Secondary combined provenance and license remain unverified; 2013–2014 annual district sources are not tied to exact official artifacts. Its 2001–2012 measures overlap the IPC file and must not be stacked as independent records. |
| `ml-model/dataset/raw/CrimesOnWomenData.csv` | **Blocked pending verification** | Exact publisher/version, license, abbreviation definitions, and state-year label semantics are unresolved. |
| `ml-model/dataset/synthetic/india_district_crime_2014_2023_30k.csv` | **Testing only** | May be used as explicitly synthetic software/UI/schema/load testing data. Must remain outside observed-data preprocessing, crime analysis, model training, tuning, and validation. |

“Blocked pending verification” is a source/rights/readiness classification, not a finding that the underlying numbers are false. The two OGD candidates remain the leading supplementary descriptive candidates, but they are not currently cleared to preprocess.

## Required preflight gates

### For either OGD/NCRB candidate

- [x] Identify the official downloads by filenames, headers, and periods; record the 2013 resource page and IPC catalog item. The IPC item's separate resource permalink was not established.
- [ ] Capture the resource's explicit license metadata and confirm its applicability to the local file. Do not infer a license from NDSAP or general site text alone.
- [x] Calculate sizes and SHA-256 for all four files, inspect encoding/headers/counts, and compare the files. The IPC hash differs but all named-field records match as an unordered multiset; the extra blank local column and row order difference are documented. The 2013 pair is byte-identical.
- [ ] Record a verified retrieval date. Observed Windows LastWriteTime values are documented as filesystem timestamps only, not proven download dates.
- [ ] Save the verified attribution statement and citation with the run manifest.
- [x] Get approval for the narrowly defined supplementary descriptive scope before preprocessing (received for Phase 2E; does not substitute for publisher license clearance).
- [ ] Define source-preserving, non-destructive outputs and test that raw input hashes remain unchanged.

### IPC district file additional gates

- [ ] Source note confirms reporting-unit scope; keep police districts/special units separate from revenue districts.
- [ ] Preserve the two `JAMMU & KASHMIR / RAILWAYS / 2010` records unchanged. Flag both as a duplicate natural-key group with unresolved reporting-unit identity; quarantine the pair from analyses requiring one observation per geography/year. Do not delete, merge, sum, average, or assign either to a revenue district without authoritative evidence.
- [ ] Classify `TOTAL`, `DELHI UT TOTAL`, and all other aggregate/special rows separately from detail.
- [ ] Keep the all-empty trailing column in the immutable raw file; any future derived-output omission must be logged and justified without changing raw data.

### 2013 state/UT file additional gates

- [ ] Keep `Total (State)`, `Total (UTs)`, and `Total (All-India)` as published aggregate records, separate from constituent State/UT detail.
- [ ] Keep IPC heads, SLL heads, and total-crimes head distinct; do not sum parent totals with components.
- [ ] Do not join the state/UT table to district records as if both had the same geography grain.

## Reviewable crosswalk templates

These templates are intentionally empty. Do not create mappings from label similarity alone. Preserve raw labels and add rows only when authoritative, year-valid evidence is recorded. Use `unresolved` or `not_assessed` rather than guessing.

### Historical state and district mapping template

| source_dataset_id | source_year_from | source_year_to | raw_state_label | raw_district_label | source_unit_kind | proposed_entity_name | official_code_system | official_code | valid_from | valid_to | relation (same/rename/split/merge/boundary_change/alias_only/unresolved) | evidence URL/document | evidence page/table | confidence | reviewer | decision/status |
|---|---:|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### Crime category mapping template

| source_dataset_id | source_year_from | source_year_to | raw_category_label | raw_law/family (if documented) | proposed_canonical_code | relation (equivalent/subcategory/parent/aggregate/distinct/unresolved) | overlap/additivity warning | official definition/source | evidence URL/page/table | confidence | reviewer | decision/status |
|---|---:|---:|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |  |

### Aggregate and subtotal classification template

| source_dataset_id | source_year | raw_geo_label | raw_category_label (if applicable) | observed total label | proposed row_type (detail/subtotal/published_total/unresolved) | parent/detail coverage | reconciliation method/result | evidence URL/page/table | confidence | reviewer | decision/status |
|---|---:|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |

### Reporting-unit classification template

| source_dataset_id | source_year | raw_state_label | raw_unit_label | proposed unit_kind (revenue_district/police_district/GRP/special_police_unit/state_total/UT_total/all_India_total/other/unresolved) | official unit identifier | parent administrative geography | valid_from | valid_to | evidence URL/page/table | confidence | reviewer | decision/status |
|---|---:|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |

## RAILWAYS duplicate preservation and quarantine specification

The local IPC and women-specific district files each have two non-identical rows under `(JAMMU & KASHMIR, RAILWAYS, 2010)`. The source pair remains unexplained. The future pipeline must:

1. Leave the source files byte-for-byte unchanged; record their verified source-file hashes in the run manifest.
2. Preserve both rows and their original source row ordinals in any derived/audit output. Do not deduplicate, overwrite, average, merge, or sum them together.
3. Mark each member of the duplicate-key group with a stable issue flag such as `duplicate_natural_key_unresolved` and a reporting-unit status `unresolved_special_reporting_unit`; flag names here are proposed metadata, not existing source columns.
4. Keep the two records in a quarantine/exception output linked to source dataset ID, file hash, and row ordinal. Never drop them silently.
5. Exclude the pair from any output that requires unique district/reporting-unit keys until an authoritative source identifies unit semantics. Their presence in published state totals does not resolve identity; do not subtract/recompute totals based on an assumed interpretation.
6. Record the unresolved question and evidence consulted in each run report. Revisit only with authoritative NCRB/state GRP documentation and explicit review.

## Crosswalk review rules

- Keep state/district name mapping separate from police/reporting-unit mapping.
- Use effective dates/reporting years and valid official code systems. A current LGD code is not by itself proof of historical boundary equivalence.
- Represent splits, mergers, and boundary changes as one-to-many or many-to-one relationships; do not collapse historical units into a modern unit automatically.
- Keep raw labels, proposed mappings, evidence, confidence, reviewer, and approval state in separate fields.
- Category mapping must be year- and law-family-aware. Never add aggregate totals to detail or parent crime heads to subcategories.

## Next approval gate

Before preprocessing, resolve the OGD item-level license metadata and exact local artifact for each candidate, then review the resulting evidence package. The next development task should be a read-only provenance reconciliation (official-file download/hash comparison and metadata capture), not preprocessing. Once both candidates pass those gates, request approval for a narrowly scoped descriptive preprocessing implementation with immutable raw inputs and the explicit exclusions above.

## Related documentation

- [Data provenance manifest](data-provenance-manifest.md)
- [Dataset eligibility matrix](dataset-eligibility-matrix.md)
- [Dataset source verification report](dataset-verification-report.md)
- [Preprocessing specification](preprocessing-plan.md)
- [Official source artifact reconciliation report](source-artifact-reconciliation-report.md)
