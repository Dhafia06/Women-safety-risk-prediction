# SafeHer Dataset Source Verification and Quality Investigation

**Phase:** 2B - source verification and detailed quality investigation
**Scope:** read-only review of the five datasets already in `ml-model/dataset/`, repository docs/Git history, and public source records. No dataset was changed, downloaded, cleaned, merged, or preprocessed.

## Executive findings

- Repository Git history contains one commit adding all five datasets (`e4357ab`, message “Add selected datasets for women safety risk analysis”). It adds no per-file source URL, license, attribution, codebook, or generation script.
- The 2013 state/UT women-crime CSV has a strong official-source match: data.gov.in lists an NCRB resource titled **Crime against Women during 2013**, annual counts in numbers, fields `State/UTs`, `Crime Head`, `2013`, and ~20 KB. Those fields and scale match the repository file. This is a structural match, not a checksum comparison.[^caw2013]
- The IPC 2001–2012 filename/title also matches an official OGD/NCRB catalog resource, with annual number figures, published in 2013 and updated in 2016. The repository file is structurally plausible, but the local 34th blank column and size discrepancy mean the exact artifact/version is not verified by byte comparison.[^ipc]
- The 2001–2014 women district file is associated by third-party references with a Kaggle upload credited to Greeshma and is described as data.gov.in/NCRB-derived. The exact original bytes, complete annual district source chain, and reuse license are not independently verified.[^kaggle2014][^gist2014]
- `CrimesOnWomenData.csv` has a matching public GitHub copy/schema and an apparent Kaggle dataset listing for 2001–2021, but no official NCRB record for this exact combined file was verified. Its local provenance and license remain unverified.[^github2021][^kaggle2021]
- No source for `india_district_crime_2014_2023_30k.csv` was found. The repository labels it synthetic, but no generator or methodology exists. It must remain isolated from observed-data analysis and model evaluation.
- The duplicate natural-key group in each district dataset is `JAMMU & KASHMIR / RAILWAYS / 2010`. The duplicate rows differ, and are included in the relevant `TOTAL` rows: every one of the 408 state-year total rows reconciles exactly against the other district-labelled rows for all numeric count columns in each file. This supports preserving the duplicate rows pending source explanation; it does not prove why the RAILWAYS reports share a label.
- Comparison of 2001–2012 district data found the two files each contain 9,017 rows and 9,016 distinct state/district/year keys. A diagnostic alias of `DELHI` to `DELHI UT` makes all keys align; all seven corresponding women-crime category value multisets then match across all 9,016 keys. This is strong evidence that the women-specific district file’s overlapping years reproduce women-related measures from the IPC table, rather than independent observations.

## 1. Repository provenance evidence

The prior inspection report records the file sizes, dimensions, headers, year coverage, and quality scans. The existing history shows a single dataset-addition commit; the repository contains no README or metadata manifest for these files. Commit history can establish when/how files entered this checkout, not who originally collected them or under what license. The file named `train_model.py` is empty, and no generation scripts are present.

The public OGD catalog identifies NCRB as contributor for its crime datasets and says that OGD-hosted data is released under NDSAP. The OGD portal states that content is owned by the publishing ministry/department and licensed under Government Open Data License–India; that license permits lawful reuse subject to attribution, non-endorsement, and its scope/exemptions.[^ogdlicense][^ogdterms] These portal terms apply only if the local artifact is indeed the resource/version covered by the OGD record. For a Kaggle/GitHub copy without exact provenance, do not assume its uploader can relicense underlying government material, and do not assume a Kaggle notebook license covers the dataset.

## 2. Dataset-by-dataset source verification

| Local file | Best source evidence | Classification and exact-copy judgment | License / attribution judgment |
|---|---|---|---|
| `optional/crcCAW_2013.csv` | Official data.gov.in resource **Crime against Women during 2013**, contributor NCRB / Ministry of Home Affairs; source stated as *Crime in India 2013*; annual figures in numbers; fields exactly `State/UTs`, `Crime Head`, `2013`; catalog says 20 KB. Local file is 20,575 bytes and 456 rows. | **Observed, official-source match strongly supported; exact byte match unverified.** Fields, period, topic, and approximate size align. No download/hash comparison was made. | OGD record says released under NDSAP; OGD platform terms identify Government Open Data License–India and require provider/source/license attribution. Confirm the individual resource license metadata at use time. Cite NCRB, *Crime in India 2013*, OGD resource URL, and license.[^caw2013][^ogdlicense] |
| `raw/01_District_wise_crimes_committed_IPC_2001_2012.csv` | Official OGD catalog resource **District-wise crime under various sections of IPC crimes during 2001–2012**, contributor NCRB, figures in numbers; catalog gives annual granularity and 995 KB. The local file has matching filename/topic/years, 9,017 rows, and 34 parsed columns (33 named columns plus a blank trailing column), 1,028,098 bytes.[^ipc] | **Observed NCRB-source family strongly supported; exact version/copy not verified.** Header/topic and dimensions are consistent with copies of this table, but no source-file checksum comparison. Police reporting unit can differ from revenue district in NCRB district tables; the catalog explicitly notes this for 2013/2014 and the local labels `RAILWAYS`, `GRP`, `STF`, etc. demonstrate that reporting units are not all ordinary administrative districts.[^ipc] | OGD page indicates NDSAP release; the platform’s current general licensing page points to Government Open Data License–India, including attribution. Verify resource metadata and retain attribution before redistribution.[^ipc][^ogdlicense] |
| `raw/crimes_against_women_2001-2014.csv` | Kaggle listing titled **Crime Against Women 2001-2014 (India)** by Greeshma exists; a public Gist points to that Kaggle page as its original dataset and documents the state/district/year and crime-count concepts. An independent project reports data.gov.in as its acquisition source, but this is secondary evidence.[^kaggle2014][^gist2014][^secondary2014] OGD’s women-crime catalog verifies separate annual 2001–2012, 2013, and 2014 resources, but the catalog copy opened describes State/UT-wise statistics, not this exact combined district file.[^womenCatalog] | **Likely observed/derived from NCRB annual statistics; exact local artifact and full district source chain unverified.** The 2001–2012 values closely reproduce matching women categories from the IPC district file (see §4). The 2013–2014 portion is not independently compared with exact official district tables. | Kaggle metadata is reported as “Other (specified in description)” by a third-party catalog, not a clear dataset license; no license file is in this repository. Treat reuse license as **unverified**. Obtain the original author’s dataset page/terms and official source attribution before redistribution.[^kaggle2014] |
| `raw/CrimesOnWomenData.csv` | Public GitHub copies show matching header (`State`, `Year`, `Rape`, `K&A`, `DD`, `AoW`, `AoM`, `DV`, `WT`) and 737-line representation, but GitHub is a mirror, not an original publisher.[^github2021] A Kaggle listing named *Crimes Against Women in India (2001-2021)* by Balaji Vara Prasad exists; third-party metadata reports Apache 2.0, but the local file is 32,551 bytes versus the listing’s reported 13,278 bytes, so artifact/version identity is not established.[^kaggle2021] NCRB publishes separate official state/UT crime-against-women tables for 2021; that does not verify this 21-year combined file.[^ncrb2021] | **Likely derived/compiled from NCRB statistics; exact origin and transformation unverified.** The 2021 endpoint and schema are consistent with NCRB-style published measures; the local state-label cardinality and casing variants need investigation. | **Unverified for this local artifact.** A mirror’s Apache listing is not sufficient to establish rights to the underlying statistics or the exact repository copy. If sourced from OGD, preserve Government Open Data License attribution; otherwise verify the uploader’s dataset-level terms first.[^kaggle2021][^ogdlicense] |
| `synthetic/india_district_crime_2014_2023_30k.csv` | No matching exact filename/source result, generator, README, metadata, or source URL found in this repository or exact-name web search. Path and filename label it `synthetic` and `30k`. | **Synthetic by repository designation; generation method and values unverified.** There is no evidence it represents observed NCRB data. Its internal rate arithmetic is consistent, but that does not establish authenticity. | **Unverified.** No creator, source license, or terms in the repository. Do not redistribute as an observed or officially licensed dataset. |

### Source research links

The primary sources most relevant to future verification are the [OGD NCRB IPC district catalog](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes), [OGD Crime against Women catalog](https://data.gov.in/catalog/crime-against-women), [OGD 2013 resource record](https://www.data.gov.in/resource/crime-against-women-during-2013), [NCRB 2013 Crime in India table index](https://www.ncrb.mha.gov.in/crime-in-india-table-content?year=2013), [NCRB 2021 table index](https://www.ncrb.mha.gov.in/crime-in-india-table-content.html?year=2021), [Government Open Data License–India](https://data.gov.in/Godl), and [OGD terms of use](https://www.data.gov.in/terms-of-use). Secondary lineage leads include the [Kaggle 2001–2014 listing](https://www.kaggle.com/datasets/greeshmagirish/crime-against-women-20012014-india), the [Gist that attributes that file to Kaggle](https://gist.github.com/lzlazmSylas/6be318f1ef48498d10f831bbd78782f3), and a [public GitHub 2001–2021 copy](https://github.com/talepa/crime_against_women_in_india_analysis_2001_2021/blob/main/CrimesOnWomenData.csv).

## 3. Synthetic dataset investigation

Measured schema: `State`, `District`, `Year`, `Crime_Type`, `Cases_Reported`, `Chargesheeted`, `Convictions`, `Population`, `Crime_Rate_per_100k`; 30,000 rows; 12 states and 300 district labels; years 2014–2023; 10 crime type strings. There are no missing fields, negative values, exact duplicate rows, or duplicate `(state, district, year, crime type)` keys in the inspected file.

The strongest direct evidence of synthetic status is its repository path/name (`dataset/synthetic/...30k.csv`). No generation code or method documentation exists. All rows obey `Chargesheeted ≤ Cases_Reported` and `Convictions ≤ Chargesheeted`; `Crime_Rate_per_100k` equals `Cases_Reported / Population × 100,000` rounded to two decimals for all rows. These constraints may reflect generated data, but arithmetic regularity alone cannot prove how the values were created. The 12-state/300-district scope, 10 crime categories, annual span, and 30,000 row count are measured; their sampling logic is unknown.

**Appropriate use:** clearly labelled UI fixtures, form/API test fixtures, schema validation, load/performance tests, and demonstrations of pipeline mechanics. Keep it in a separate partition with explicit synthetic provenance. Do not use it as crime evidence, real-world baseline, model target, external validation, or a supplement merged into observed records.

## 4. Duplicate natural-key investigation

Both datasets contain a single duplicate key group. The key is `(state, district, year) = (JAMMU & KASHMIR, RAILWAYS, 2010)` with two rows in each file.

### IPC district file

The rows are identical for 21 columns: state, district, year, the blank index, and 17 count columns. They differ in these 13 count columns (row values shown in file order):

| Column | Values |
|---|---|
| `MURDER` | 0, 1 |
| `CULPABLE HOMICIDE NOT AMOUNTING TO MURDER` | 0, 1 |
| `RAPE` | 0, 1 |
| `OTHER RAPE` | 0, 1 |
| `KIDNAPPING & ABDUCTION` | 1, 0 |
| `KIDNAPPING AND ABDUCTION OF OTHERS` | 1, 0 |
| `BURGLARY` | 1, 0 |
| `THEFT` | 12, 8 |
| `OTHER THEFT` | 11, 7 |
| `RIOTS` | 16, 0 |
| `CRIMINAL BREACH OF TRUST` | 1, 0 |
| `OTHER IPC CRIMES` | 5, 10 |
| `TOTAL IPC CRIMES` | 36, 21 |

### Women district file

The two rows share state, district, year, and six of seven crime measures. The blank index-like field is `6880` vs `6881`; `Rape` is `0` vs `1`. Other category counts are identical.

### Interpretation and handling

The natural key is not unique, but the rows are not exact duplicates. `RAILWAYS` occurs as a reporting label and likely represents police/reporting jurisdictions rather than a standard revenue district; the local data cannot tell whether the two rows represent separate railway units collapsed to one name, a source correction, or an error. No codebook/source note found resolves this. Crucially, each file’s 408 `TOTAL` state-year rows equals the sum of all other district-labelled rows for every numeric count column, including both RAILWAYS rows. That supports retaining both in a faithful source reconstruction while flagging them; deleting one would break the measured reconciliation. Do not average or deduplicate. Quarantine/flag the shared key and seek original workbook notes or NCRB reporting-unit detail before assigning a finer unit ID.

## 5. Aggregate/subtotal investigation

| File | Aggregate labels/counts observed | Reconciliation / overlap evidence |
|---|---|---|
| `crcCAW_2013.csv` | `Total (State)`, `Total (UTs)`, and `Total (All-India)`: 12 rows each, 36 total-like rows across 12 crime heads. | For all 12 crime heads, `Total (All-India)` equals `Total (State)` + `Total (UTs)` and also equals the sum of all other state/UT-labelled rows. This is a measured reconciliation; retain totals separately from detail. |
| IPC 2001–2012 | `DISTRICT=TOTAL`: 408 rows (34 state/year groups × 12 years); `DELHI UT TOTAL`: 12 rows (one per Delhi UT/year, 2001–2012). | For every `TOTAL` row, all 30 numeric columns exactly equal the sum of same-state/year rows whose district label is not total-like. All 12 `DELHI UT TOTAL` rows also match all 30 columns summed over Delhi detail rows. |
| Women district 2001–2014 | `TOTAL`: 408 rows (34 state/year groups, 2001–2012); `DELHI UT TOTAL`: 12 rows (2001–2012); `ZZ TOTAL`: 35 rows (one per state/UT in 2013); `Total District(s)`: 36 rows (one per state/UT in 2014). | All 408 `TOTAL` rows match all seven categories summed over non-total-like rows in the same state/year. The 12 Delhi totals, 35 `ZZ TOTAL` rows, and 36 `Total District(s)` rows also each match all seven category sums over other same-state/year rows. The labels differ by year but behave as aggregates in these checks; preserve/flag, and do not count them alongside detail. |
| State-year women file 2001–2021 | No `total`-named state labels were detected by the previous inventory, but 70 distinct state strings exist over 21 years; row-by-row label review remains warranted. | Do not infer that it lacks national aggregates from the string heuristic alone; verify labels during a source-backed quality pass. |
| Synthetic district file | No aggregate-like district labels were detected. | No observed-data reconciliation is appropriate. |

NCRB’s official tables distinguish state/UT and city tables, and official district table notes may include special police units; a reporting jurisdiction should not be treated as a district without checking the source table legend.[^ipc][^ncrb2013] During preprocessing, use an explicit record-level geographic-unit type, retain raw labels, and keep aggregate records in a separate table/flag. Compute totals from detail rows once, never add published totals to their components.

## 6. Geographic names and join-key risks

Measured issues:

- In `crimes_against_women_2001-2014.csv` and `CrimesOnWomenData.csv`, 33 normalized state/UT labels each occur with both uppercase and title-case spellings. This is a formatting-only difference where strings normalize identically by trim + whitespace collapse + case-fold.
- The 2001–2012 IPC file uses `DELHI UT`, while the women district file uses `DELHI`. These labels are not just casing; they require an explicit, time-aware alias decision. For diagnostic comparison only, treating them as aliases aligns all 9,016 unique keys; do not silently overwrite raw labels.
- District names are not unique nationally. The IPC file has 13 normalized district-label groups occurring across multiple state/reporting labels; the women district file has 42. Examples include generic directions (`NORTH`, `SOUTH`, `EAST`, `WEST`), `RAILWAYS`, `GRP`, `TOTAL`, and same-name districts. Always use at least state/reporting unit + district + year, then use official geographic/reporting-unit IDs when available.
- The 2001–2012 women file has 72 distinct state/UT strings due to formatting and aggregate/administrative labels. `CrimesOnWomenData.csv` has 70; that count is not an official-jurisdiction count.
- Names such as `JAMMU & KASHMIR`, `A & N ISLANDS`, `D & N HAVELI`, `DAMAN & DIU`, `ORISSA`/`ODISHA` (where present across sources), and newer state/UT reorganizations require date-aware authoritative crosswalks. Only some are confirmed in this local scan; no mapping is presumed here.
- Historical state creation and district boundary/name changes mean identical labels across years do not guarantee stable areas. A historical crosswalk by year is required before longitudinal district comparisons.

### Proposed standardization strategy (not applied)

1. Preserve every raw state/district string in immutable source columns.
2. Add normalized comparison labels using Unicode normalization, trimming, whitespace collapse, and case-folding only; treat this as formatting normalization, not geographic identity.
3. Resolve aliases and administrative changes via an authoritative, dated Government of India Local Government Directory or official NCRB reporting-unit crosswalk. Record effective dates and source citations.
4. Distinguish district, city, railway police, special unit, state/UT total, and all-India total with a `geography_level`/`unit_type` field; never map special police units to revenue districts by guess.
5. Join with stable code + validity period when available; quarantine unresolved mappings and same-name cross-state districts.

## 7. Crime category / reporting-definition findings

The IPC table contains general IPC offense counts and women-related categories together. A column name can be mapped syntactically to a women-specific column, but category scope should be proven using the annual report glossary/table notes. For 2001–2012, category values provide strong evidence of shared measure lineage: on all 9,016 keys after the diagnostic Delhi alias, the seven women categories match as multisets. `Kidnapping and Abduction` in the women-specific file matches `KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS`, not the broader `KIDNAPPING & ABDUCTION` column, in the IPC file. The broad column includes other kidnapping/abduction components, so using it would change the measure.

Potential hierarchy/double counting in the IPC file includes `RAPE` alongside `CUSTODIAL RAPE` and `OTHER RAPE`, broad `KIDNAPPING & ABDUCTION` alongside women/girls and others components, `THEFT` alongside auto/other theft, and `TOTAL IPC CRIMES` alongside all component offense heads. Do not sum parent and child categories. The seven women measures also should not be summed to a single “women’s crime” total without confirming mutually exclusive counting and legal/reporting definitions.

`CrimesOnWomenData.csv` abbreviations appear to correspond to seven measures (Rape; Kidnapping & Abduction; Dowry Deaths; Assault on women with intent to outrage her modesty; Insult to modesty of women; Cruelty by husband/relatives; Importation of girls), but the file has no codebook. These expansions are hypotheses from related file headers and matching copies, not a verified local data dictionary. See `docs/data-dictionary.md` for column-by-column status.

## 8. Dataset compatibility matrix

| Pair | Assessment | Evidence / risk | Recommendation |
|---|---|---|---|
| IPC 2001–2012 ↔ women district 2001–2014 | **Conditionally compatible; overlapping measures appear identical** | Same 9,017 row count over years 2001–2012; after diagnostic `DELHI`/`DELHI UT` alias, all 9,016 composite keys align and all seven women measures match. Duplicate RAILWAYS key remains; aggregate records are included in reconciliation. | Do not merge as independent observations. Use one verified source as the canonical panel, and retain the other as a validation/reference copy only after confirming official provenance/version. |
| Women district 2001–2014 ↔ state women 2001–2021 | **Insufficient evidence / conditionally comparable after aggregation** | Overlapping years and category concepts; district file includes police/reporting-unit labels and aggregates; state file’s abbreviations/state aliases lack a data dictionary. Potentially derived from related NCRB data. | Compare only after authoritative category and state crosswalks; aggregate district detail without published subtotal rows and reconcile to official state totals. |
| IPC 2001–2012 ↔ state women 2001–2021 | **Conditionally compatible for selected women measures** | Shared annual category measures; geography resolution differs; overlapping source likely. IPC broader parent categories can be mistaken for women-only values. | Compare selected verified subcategory columns only; never add them as new records. |
| OGD 2013 `crcCAW` ↔ any earlier/later women table | **Conditionally compatible** | Official annual NCRB/OGD provenance for 2013, but long-format state/crime-head table, explicit total rows, and label/category versions need crosswalk. | Use as a one-year supplemental reconciliation point after codebook/total handling; do not concatenate without provenance and category mapping. |
| Synthetic district 2014–2023 ↔ any observed dataset | **Incompatible for evidentiary analysis; compatible only as a software fixture** | Synthetic designation and undocumented generator; shared-looking categories/geography do not make records real. | Keep fully isolated; no merge, training, validation, or calibration. |

## 9. Provisional primary dataset selection

No fully verified primary dataset is selected. Candidate order for further validation:

1. **Primary candidate pending source/license verification:** `crimes_against_women_2001-2014.csv`. It is directly relevant, district-labelled, annually spans 14 years, is complete under the mechanical null scan, and its 2001–2012 rows match the corresponding women categories in the IPC file. Its exact provenance, 2013–2014 official district table match, and dataset license remain unverified. It lacks population/exposure denominators and is not incident-level.
2. **Official-source supplementary/reference candidate:** `01_District_wise_crimes_committed_IPC_2001_2012.csv`. OGD/NCRB source family is well supported. It offers broad district/reporting-unit crime counts and a women-related subset, but the 2012 cutoff, general IPC scope, total/category hierarchy, blank header, and special reporting units limit use as the sole women-focused source.
3. **Supplementary official one-year check:** `crcCAW_2013.csv`, strong OGD/NCRB structural match, state/UT-level annual count matrix. One year is insufficient for primary longitudinal use; its explicit aggregate rows need exclusion/flags for detail analysis.
4. **Supplementary candidate pending verification:** `CrimesOnWomenData.csv`, state-level 2001–2021 and relevant categories. Longer time coverage is attractive, but the exact local source, category abbreviations, state labels, and license are unresolved; it cannot be used as a verified evaluation set yet.
5. **Development/testing only:** `india_district_crime_2014_2023_30k.csv`. Keep isolated as synthetic; not a primary or supplementary evidence dataset.

Because observed files lack population/exposure measures, no crime rate normalization is available from the observed data alone. Reported crime counts measure registered/reporting volume under particular definitions, not personal probability of harm or safety. A target and validation plan must be established before model selection.

## 10. Blocking questions and next steps

1. Obtain the original NCRB/OGD source artifacts and compare byte hashes or complete parsed data to each local file; record retrieval date and version without replacing repository files.
2. Confirm dataset-level license metadata for every exact resource and Kaggle artifact; add explicit attribution before public redistribution.
3. Obtain original report table notes/codebooks, especially the meaning of district versus police unit, `RAILWAYS`, `TOTAL`, `ZZ TOTAL`, `Total District(s)`, and 2013 category definitions.
4. Resolve the Delhi alias and create a dated state/UT and reporting-unit crosswalk. Establish whether the RAILWAYS duplicate rows represent separate reporting jurisdictions.
5. Verify 2013/2014 district women rows against their exact NCRB district table sources; investigate whether the state-wide `CrimesOnWomenData.csv` is internally consistent with official NCRB tables, including state attribution.
6. Locate or document the generator and license for the synthetic file, or continue treating it strictly as an unverified fixture.
7. Decide the narrow descriptive prediction target and what observed-data time/geographic holdout can validly evaluate it. Source a compatible population/exposure denominator if rates are needed.

Preprocessing remains blocked on source/version/license and special-unit semantics. No cleaning, mapping, joining, or model work was done in this phase.

## Sources and citations

[^caw2013]: OGD India, [Crime against Women during 2013](https://www.data.gov.in/resource/crime-against-women-during-2013), records source as *Crime in India 2013*, NCRB; annual figures in numbers; fields and file size shown in the resource metadata. OGD [Crime against Women catalog](https://data.gov.in/catalog/crime-against-women) lists the NCRB as contributor and separate 2001–2012, 2013, and 2014 resources.
[^ipc]: OGD India, [District-wise crimes under various sections of IPC crimes](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes), NCRB contributor, annual figures, catalog dates, and source notes. Search result/catalog content includes the 2001–2012 resource and describes the source as *Crime in India 2012*, NCRB.
[^womenCatalog]: OGD India, [Crime against Women catalog](https://data.gov.in/catalog/crime-against-women), describing state/UT-wise crime heads, NCRB contribution, and separate 2001–2012, 2013, and 2014 resources.
[^ncrb2013]: NCRB, [Crime in India 2013 table contents](https://www.ncrb.mha.gov.in/crime-in-india-table-content?year=2013), listing separate state/UT/city and district crime tables.
[^ncrb2021]: NCRB, [Crime in India 2021 table contents](https://www.ncrb.mha.gov.in/crime-in-india-table-content.html?year=2021), listing official state/UT crime-against-women tables.
[^ogdlicense]: OGD India, [Government Open Data License–India](https://data.gov.in/Godl), which sets reuse conditions and attribution for covered shareable government data.
[^ogdterms]: OGD India, [Terms of Use](https://www.data.gov.in/terms-of-use), which says portal content is owned by the respective publishers and licensed under Government Open Data License–India, subject to dataset metadata/third-party materials.
[^kaggle2014]: Kaggle, [Crime Against Women 2001–2014 (India)](https://www.kaggle.com/datasets/greeshmagirish/crime-against-women-20012014-india). The page is identifiable, but content/license metadata could not be independently read from the page in this inspection.
[^gist2014]: Public [Gist mirror and attribution note](https://gist.github.com/lzlazmSylas/6be318f1ef48498d10f831bbd78782f3) linking the 2001–2014 file to the Kaggle upload and describing fields. Secondary lineage evidence only.
[^secondary2014]: Secondary report stating its 2001–2014 district/state data was acquired from data.gov.in: [project report](https://www.nkc.ac.in/AQAR-23-24/AQAR_2023-24_MSc_IT_Sem_III_P_12.pdf). It does not verify the local artifact/hash.
[^github2021]: Public [GitHub mirror of `CrimesOnWomenData.csv`](https://github.com/talepa/crime_against_women_in_india_analysis_2001_2021/blob/main/CrimesOnWomenData.csv) with matching field names and 737 lines. It is not the original publisher.
[^kaggle2021]: Kaggle, [Crimes Against Women in India (2001–2021)](https://www.kaggle.com/datasets/balajivaraprasad/crimes-against-women-in-india-2001-2021). A third-party metadata index reports Apache 2.0 and a materially different byte count; exact local version and rights are unverified.

## 10. Phase 2B follow-up: final eligibility and definition review

**Review date:** 2026-11-28. This is a documentation-only follow-up. No CSV was changed, downloaded, cleaned, joined, or transformed. Local category vocabularies were read only to make the comparison below. Repository files have not been checksum-compared against publisher downloads; no legal opinion is provided.

### Source versions, publishers, and reuse status

| Local dataset | Best supported original source/version and publisher | Exact local artifact? | License and attribution conclusion |
|---|---|---|---|
| `optional/crcCAW_2013.csv` | OGD resource **Crime against Women during 2013**, contributor NCRB / Ministry of Home Affairs, explicitly sourced to *Crime in India 2013*. Fields, year, topic, and approximate 20 KB size align with the local file. | Strong structural match; no publisher download/checksum comparison. | OGD's terms say dataset-record license metadata controls; covered OGD data is under GODL-India and requires provider, source, license, and resource URL attribution. The local file's record-specific license metadata was not captured, so retain that verification caveat. |
| `raw/01_District_wise_crimes_committed_IPC_2001_2012.csv` | OGD/NCRB catalog resource **District-wise crime under various sections of IPC crimes during 2001–2012**, annual figures; NCRB is the contributor and *Crime in India 2012* is identified as source in the catalog trail. | Source family strongly supported; local size/blank trailing column prevents exact artifact assertion; no checksum comparison. | GODL-India is the applicable OGD platform framework when the individual resource record licenses the artifact. Capture that record's license metadata and use explicit attribution before redistribution. |
| `raw/crimes_against_women_2001-2014.csv` | Secondary lineage points to Greeshma's Kaggle dataset; NCRB's annual 2001–2012, 2013, and 2014 releases are separate plausible upstream sources. The local file reproduces the IPC file's seven women-related fields for all aligned 2001–2012 keys. | Not verified. The 2013–2014 district components and the combination/export process are not reconciled to exact official district source tables. | Kaggle page terms/license could not be independently verified for this local combined artifact. Do not treat OGD rights as inherited without proof that each source artifact is the covered OGD resource. Uploader authority over underlying data also remains unresolved. |
| `raw/CrimesOnWomenData.csv` | Matching GitHub mirror and a Kaggle listing by Balaji Vara Prasad are secondary lineage only. NCRB state/UT annual source tables exist, but no official publisher record for this exact 2001–2021 combined file was identified. | Not verified; local size differs materially from the Kaggle size reported in existing research. | Unverified for this artifact. A third-party listing's reported Apache label is not evidence of rights in the underlying NCRB data or this local copy. |
| `synthetic/india_district_crime_2014_2023_30k.csv` | No publisher, upstream version, generator, or source found. `synthetic` is a repository classification, not provenance evidence by itself. | No source artifact to match. | No creator license/terms found. Do not redistribute as official/observed data. Use only as an explicitly synthetic local software fixture. |

For the two OGD candidates, official-source identity is stronger than the two secondary copies, but exact local version and record-level license metadata remain open verification items. The official portal says content is owned by the respective provider, individual record license metadata governs, and reproduction requires acknowledgment; GODL-India's template calls for provider, year, dataset, repository/version, URL, and license. A citation to a catalog is not a substitute for confirming the resource record and artifact lineage. [OGD terms](https://www.data.gov.in/terms-of-use), [GODL-India](https://data.gov.in/Godl).

### RAILWAYS duplicate: evidence and limits

NCRB's 2012 table index has a distinct **Crime in Railways** section with GRP IPC tables for 2010, 2011, and 2012, alongside the district-wise IPC table. Separately, the OGD catalog's district-table note for later editions says its “districts” are police districts and include special police units, which may differ from revenue districts. This establishes that railway/GRP policing is a distinct reporting domain and district-table geography is not necessarily revenue geography. It does **not** establish that the two local Jammu & Kashmir `RAILWAYS` rows are two distinct GRP units.

No public table note found explains the duplicate pair's same state / same district-label / same year key or its differing counts. Available evidence is consistent with multiple railway reporting units collapsed to one label, a duplicated/variant source record, or a source correction; none is verified. The local aggregate reconciliation that includes both rows supports preserving the source as published, not selecting an interpretation. **Conclusion:** `RAILWAYS` should be typed as a special police/reporting-unit label candidate, not mapped to a revenue district; the two rows remain unresolved and must not be deleted, merged, or averaged. Quarantine this key from analyses that require a unique geography until NCRB's source workbook/notes or state/GRP detail identifies the units.

Primary references: [NCRB 2012 table contents](https://www.ncrb.mha.gov.in/crime-in-india-table-content?year=2012), including separate GRP tables; [OGD IPC catalog](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes), including the police-district/special-unit note for its later district resources.

### Proposed year-aware geographic crosswalk (not applied)

Do not create a single timeless `state,district -> geography` lookup. Proposed crosswalk rows should carry source dataset/version, raw label, entity kind (`state_ut`, `revenue_district`, `police_district`, `GRP/special_unit`, `published_total`, `unresolved`), valid-from/to dates or reporting years, authoritative identifier and source, mapping relation (`same`, `rename`, `split`, `merge`, `boundary_change`, `alias_only`, `unresolved`), and evidence/confidence. Use raw-label + year + reporting-unit type as lookup context. Preserve one-to-many and many-to-one events; never force a split/merge into a one-to-one join.

| Period/event | Proposed handling in these files |
|---|---|
| Jharkhand, Chhattisgarh, and Uttarakhand were created in 2000; all observed-file periods start in 2001. | Treat their state labels as their post-creation jurisdictions for the observed years, but do not backcast predecessor-state boundaries into district time series without an official district-level boundary lineage. |
| `ORISSA` / `ODISHA` (if present in source labels): the state name changed, while same-year official labels must be retained. | Candidate state-level `rename` alias only after confirming the label's official period and that it refers to the same state territory. Preserve the source spelling. |
| `UTTARANCHAL` / `UTTARAKHAND` (if present): the state name was changed to Uttarakhand effective 2007-01-01. | Candidate state-level rename alias for identity continuity, retaining raw spelling and reporting year. Confirm each source's label convention; do not assume the same district structure. |
| Andhra Pradesh / Telangana, Telangana formed 2014. | Keep as separate jurisdictions from 2014 onward. Treat 2014 as a transition-year source definition requiring the annual report's treatment; do not reassign Telangana districts into AP or compare the 2014 observations as a clean pre/post panel without NCRB notes. |
| Former Jammu & Kashmir state reorganized into UT Jammu & Kashmir and UT Ladakh effective 2019-10-31. | Pre-change annual labels refer to former J&K as reported. 2019 is a transition-year ambiguity. From 2020, preserve successor labels; never split historical J&K counts into the successor UTs absent source unit data. |
| Dadra and Nagar Haveli and Daman and Diu merged effective 2020-01-26. | Keep pre-merger series separately. Treat 2020 as transition year. Combine the pre-merger areas only for a specifically approved comparable-area view and only if source reporting covers both; do not overwrite original identities. |
| District names, districts created/abolished, and boundary changes within states. | Use dated official district/revenue records and the reporting-year source table. Census 2011 codes identify that vintage, not automatically all 2001–2021 boundaries. Current LGD provides unique codes and supports administrative updates/versioning, but a current directory alone is not a historical boundary crosswalk. |
| NCRB police districts, GRP/Railways, STF, totals, and other special labels. | Keep a separate reporting-unit namespace. Map to revenue geography only with explicit NCRB/state police documentation. Keep `TOTAL` and analogous rows as published aggregates, never as districts. |

Official anchors include MHA's [Jammu & Kashmir/Ladakh formation and 2019-10-31 date](https://mha.gov.in/index.php/jammu-kashmir-ladakh-affairs), MHA's [UT reorganization summary](https://www.mha.gov.in/web/sites/default/files/MHAARE_22042022%5B1%5D.pdf) noting the J&K/Ladakh and DNH/DD effective dates, Ministry of Panchayati Raj's [LGD description](https://panchayat.gov.in/lgd/) of unique codes for current/new entities and reorganization, and OGD's [LGD catalog](https://data.gov.in/catalog/local-government-directory-lgd) with district-code resources updated monthly. The geographic crosswalk remains a proposal; these references do not resolve each local district row or police unit.

Additional official historical anchors: the [Census of India Administrative Atlas](https://censusindia.mha.gov.in/census.website/data/atlas) documents district creations between Census 2001 and 2011; the [Government of Telangana state profile](https://www.telangana.gov.in/about/state-profile/) dates state formation to 2014-06-02; the [Government of Odisha reference](https://magazines.odisha.gov.in/orissaannualreference/ORA-2011/pdf/orissa%20reference%20annual-2011.pdf) records the Orissa-to-Odisha change taking effect 2011-11-01; official sources state [Uttaranchal's name changed to Uttarakhand in 2007](https://rajbhavan.mizoram.gov.in/raj-bhavan-mizoram-hosts-observation-of-formation-day-of-jharkhand-and-uttarakhand-states/); and PIB states [Chhattisgarh/Jharkhand formed in November 2000](https://www.pib.gov.in/newsite/erelcontent.aspx?lang=2&reg=48&relid=18420), while Uttarakhand's Chief Minister office records its [formation on 2000-11-09](https://cm.uk.gov.in/geography/). These dates set candidate state-level intervals only; they do not produce a district boundary crosswalk.

### Crime-category comparison

This is a semantic crosswalk proposal, not permission to combine counts. The 2015 NCRB methodology describes gender-specific IPC heads separately from SLL heads, describes legal-section coverage, notes a revised reporting proforma, and identifies new categories; category names and scope therefore must be versioned by year. [NCRB Crime in India 2015, Chapter 5](https://www.ncrb.mha.gov.in/uploads/2022/July/11/custom/crime-in-india/chapter-5-15.11.16_2015.pdf).

| Category relationship | Evidence-based comparison | Safe handling |
|---|---|---|
| Strong overlapping women-specific district equivalents | Women district columns `Rape`, `Kidnapping and Abduction`, `Dowry Deaths`, assault, insult, cruelty, and importation match their corresponding IPC columns for every aligned 2001–2012 key per local comparison. The kidnapping counterpart is `KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS`, not broad `KIDNAPPING & ABDUCTION`. | Candidate one-to-one comparison within 2001–2012 only, pending official vintage/codebook confirmation. Do not append/stack matching files as independent observations. |
| 2013 state table equivalents by label | `Rape`, women-and-girls kidnapping & abduction, dowry deaths, assault on women, insult to modesty, cruelty, and importation appear conceptually comparable to women-specific IPC heads. Local labels include source typos/truncations (`Grils`, `Modest`) and legal wording/scope must be checked against 2013 tables. | Candidate label mappings only; keep raw categories and table-version provenance. 2013 is state/UT aggregated and cannot be joined to district rows as the same grain. |
| State-year abbreviation candidates | `Rape` is explicit. `K&A`, `DD`, `AoW`, `AoM`, `DV`, and `WT` are unexpanded in the local source. Some expansions are plausible, but `DV` must not be assumed to equal IPC cruelty and `WT` must not be assumed to equal importation or Immoral Traffic. | Leave abbreviations unmapped until the exact publisher data dictionary/source is found. Even apparent label equivalents are not locally verified. |
| IPC parents and subcategories | Broad `KIDNAPPING & ABDUCTION` coexists with women/girls and others subheads. `RAPE` coexists with `CUSTODIAL RAPE` and `OTHER RAPE`. `THEFT` coexists with `AUTO THEFT` and `OTHER THEFT`. Other total/residual fields may also overlap. | Treat parent and child fields as potentially overlapping/hierarchical. Never sum parent with components. Verify each year's table notes first. |
| Aggregate heads | `TOTAL IPC CRIMES`, 2013 `Total Crimes against Women`, and explicit state/UT/all-India totals summarize underlying categories/geographies. | Aggregates are not additive features alongside their components; preserve as published totals in a separate aggregate type. |
| SLL categories in 2013 | The 2013 local file also contains Dowry Prohibition Act, Immoral Traffic (P) Act, Commission of Sati (P) Act, and Indecent Representation of Women (P) Act heads. These are separate statutory categories, not interchangeable with the seven IPC heads. | Keep separate law-family/category codes. Do not combine with IPC-only totals unless official table definition explicitly says the total covers both; the total itself remains an aggregate. |
| Synthetic labels | Generic `Assault`, `Kidnapping`, etc. lack legal definitions, while observed tables use offence heads and period-specific law sections. | No observed-category crosswalk. Keep for software fixtures only. |

### Final eligibility decisions

The fuller per-file matrix is in [`dataset-eligibility-matrix.md`](dataset-eligibility-matrix.md). No dataset is cleared as a primary predictive-analysis source. The IPC district and 2013 state/UT OGD files are candidates for **supplementary descriptive** use, subject to record-license confirmation, provenance citation, exclusion/typing of totals and special units, and appropriate geography scope. The synthetic file is restricted to software testing. The two secondary combined files remain quarantined for analytical use until exact lineage, definitions, and rights are verified.
