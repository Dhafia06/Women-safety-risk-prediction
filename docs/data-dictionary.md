# SafeHer Crime Dataset Data Dictionary

This dictionary describes the columns measured in the local files. Definitions are classified as **verified source description**, **header-derived**, or **unverified**. A plausible expansion is not treated as an authoritative legal definition. All four files under `raw/`/`optional/` contain aggregate statistics, not person-level incident records. The `synthetic/` file is kept separate.

## `ml-model/dataset/optional/crcCAW_2013.csv`

Official OGD metadata identifies the resource as *Crime against Women during 2013*, annual, with figures in numbers and fields `State/UTs`, `Crime Head`, `2013`.[^2013]

| Original column | Observed type | Meaning / unit / role | Total/subcategory and cross-file relationship | Status |
|---|---|---|---|---|
| `State/UTs` | Text/category | State/Union Territory label. Not a stable code. | Geography dimension; comparable in concept to `STATE/UT` and `State` after a sourced time-aware alias table. | Meaning verified by OGD metadata; identity mapping not verified. |
| `Crime Head` | Text/category | NCRB crime-head label. | One row per state/UT × crime head; labels may correspond to some women-crime fields elsewhere. Totals are separate crime heads and must be flagged. | Meaning verified at high level; each exact definition requires Crime in India 2013 glossary. |
| `2013` | Numeric/integer-like | Number of reported/recorded cases for that crime head and state/UT in 2013. | Measure, not a year-valued observation column after later normalization. Category may be a total or component depending on `Crime Head`. | OGD says figures are in numbers; precise case/incident wording should follow source table notes. |

## `ml-model/dataset/raw/01_District_wise_crimes_committed_IPC_2001_2012.csv`

OGD identifies an annual NCRB district-wise IPC crime table and states that figures are in numbers.[^ipc] There are 34 CSV columns, including a blank trailing header whose cells are all empty.

| Original column | Observed type | Meaning / unit / role | Total/subcategory and cross-file relationship | Status |
|---|---|---|---|---|
| `STATE/UT` | Text/category | State/UT reporting label. | Geography/reporting jurisdiction; not a stable ID. Equivalent in concept to `STATE/UT` in women file and state columns in other tables. | Header/source-level meaning; alias mapping unverified. |
| `DISTRICT` | Text/category | District/reporting-unit label for the row. | Geography dimension. Labels include ordinary district names, railway/special-unit-like names, and subtotal labels. | Header-derived; official note distinguishes reporting units from revenue districts in related NCRB tables. Exact unit per label needs source codebook. |
| `YEAR` | Numeric/integer-like | Calendar/reporting year 2001–2012. | Time dimension; annual. | Verified from values and title. |
| `MURDER` | Numeric/integer-like | Count under the named IPC crime head. | General IPC crime measure; not a women-only field. | Header-derived; exact scope should use NCRB glossary. |
| `ATTEMPT TO MURDER` | Numeric/integer-like | Count under named IPC crime head. | General IPC crime measure. | Header-derived. |
| `CULPABLE HOMICIDE NOT AMOUNTING TO MURDER` | Numeric/integer-like | Count under named IPC crime head. | General IPC crime measure. | Header-derived. |
| `RAPE` | Numeric/integer-like | Count under rape head. | Women-specific concept; matches `Rape` in the 2001–2014 women district file across overlapping keys in this local comparison. Also has `CUSTODIAL RAPE` and `OTHER RAPE` columns; do not sum parent and components. | Local cross-file equality measured; legal scope still report-defined. |
| `CUSTODIAL RAPE` | Numeric/integer-like | Count under named rape subhead. | Likely component of `RAPE`; aggregation hierarchy must be confirmed. | Header-derived; hierarchy needs source glossary. |
| `OTHER RAPE` | Numeric/integer-like | Count under named rape subhead. | Likely component of `RAPE`; do not add to RAPE without verification. | Header-derived; hierarchy needs source glossary. |
| `KIDNAPPING & ABDUCTION` | Numeric/integer-like | Count under broad kidnapping/abduction head. | Broader than the women-specific `Kidnapping and Abduction` measure: local equality is with `KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS`, not this broader column. Parent/child relation must be verified before summing. | Local comparison measured; definition needs NCRB glossary. |
| `KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS` | Numeric/integer-like | Count under named women/girls subhead. | Matches the women file’s `Kidnapping and Abduction` count at all matched 2001–2012 keys. Likely a component of broad kidnapping/abduction. | Local equality measured; formal definition is report-dependent. |
| `KIDNAPPING AND ABDUCTION OF OTHERS` | Numeric/integer-like | Count under named other-person subhead. | Likely another component of broad kidnapping/abduction. | Header-derived; source glossary required. |
| `DACOITY` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header-derived. |
| `PREPARATION AND ASSEMBLY FOR DACOITY` | Numeric/integer-like | Count under named IPC head. | Related to dacoity; not safe to aggregate with `DACOITY` without definitions. | Header-derived. |
| `ROBBERY` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header-derived. |
| `BURGLARY` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header-derived. |
| `THEFT` | Numeric/integer-like | Count under named IPC head. | Coexists with `AUTO THEFT` and `OTHER THEFT`; possible hierarchy/overlap. | Header-derived; hierarchy requires glossary. |
| `AUTO THEFT` | Numeric/integer-like | Count under named IPC head. | Possible component of theft. | Header-derived. |
| `OTHER THEFT` | Numeric/integer-like | Count under named IPC head. | Possible component of theft. | Header-derived. |
| `RIOTS` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header-derived. |
| `CRIMINAL BREACH OF TRUST` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header-derived. |
| `CHEATING` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header-derived. |
| `COUNTERFIETING` | Numeric/integer-like | Count under spelling as present in source. | General IPC crime measure. | Header typo retained in source; exact intended label should be confirmed from official table. |
| `ARSON` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header-derived. |
| `HURT/GREVIOUS HURT` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header spelling retained; exact scope needs glossary. |
| `DOWRY DEATHS` | Numeric/integer-like | Count under named women-crime head. | Matches `Dowry Deaths` in the women district table at all matched 2001–2012 keys. | Local equality measured; exact legal/report scope from annual glossary. |
| `ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY` | Numeric/integer-like | Count under named women-crime head. | Matches same-named measure in women district table at all matched 2001–2012 keys. | Local equality measured; legal scope may evolve. |
| `INSULT TO MODESTY OF WOMEN` | Numeric/integer-like | Count under named women-crime head. | Matches `Insult to modesty of Women` in women district table at all matched keys. | Local equality measured; legal scope may evolve. |
| `CRUELTY BY HUSBAND OR HIS RELATIVES` | Numeric/integer-like | Count under named women-crime head. | Matches women district table at all matched keys. | Local equality measured; legal scope may evolve. |
| `IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES` | Numeric/integer-like | Count under named women-crime head. | Matches `Importation of Girls` in women district table at all matched keys. | Local equality measured; formal label differs. |
| `CAUSING DEATH BY NEGLIGENCE` | Numeric/integer-like | Count under named IPC head. | General IPC crime measure. | Header-derived. |
| `OTHER IPC CRIMES` | Numeric/integer-like | Count in residual/other IPC category. | May aggregate multiple other categories; do not sum with constituent measures unless specified. | Header-derived; residual definition unverified. |
| `TOTAL IPC CRIMES` | Numeric/integer-like | Published total IPC count for the reporting unit/year. | Aggregate total; overlaps component crime heads. Never add to components. | Header-derived; official total definition must be checked. |
| blank final header | Empty/text | No populated values in local file; likely trailing CSV delimiter/artifact. | Not a feature or identifier unless source version proves otherwise. | Measured all 9,017 cells blank; removal only in approved preprocessing. |

## `ml-model/dataset/raw/crimes_against_women_2001-2014.csv`

| Original column | Observed type | Meaning / unit / role | Total/subcategory and cross-file relationship | Status |
|---|---|---|---|---|
| blank first header | Numeric-looking | Sequential/index-like value (not a documented identifier). | No reliable join key; local row values are unique but that does not establish semantic meaning. | Likely export index; unverified. |
| `STATE/UT` | Text/category | State/UT or source reporting label. | Geography dimension; `DELHI` appears in this file where IPC file has `DELHI UT`; 33 state labels also vary by casing. | Observed variants measured; historical alias needs dated crosswalk. |
| `DISTRICT` | Text/category | District/reporting-unit label. | Includes `TOTAL`, `DELHI UT TOTAL`, `ZZ TOTAL`, `Total District(s)`, and special reporting-unit labels; not all rows are administrative districts. | Header-derived; labels measured, semantics not resolved. |
| `Year` | Numeric/integer-like | Annual period 2001–2014. | Time dimension. | Verified from values. |
| `Rape` | Numeric/integer-like | Count for rape head. | Matches IPC `RAPE` at overlapping keys. | Local equality measured; legal scope source-defined. |
| `Kidnapping and Abduction` | Numeric/integer-like | Women/girls kidnapping and abduction count in this table’s category scheme. | Matches IPC `KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS`, not broad `KIDNAPPING & ABDUCTION`, across overlapping keys. | Local equality measured; original Kaggle description is secondary. |
| `Dowry Deaths` | Numeric/integer-like | Count for dowry deaths. | Matches IPC `DOWRY DEATHS`. | Local equality measured. |
| `Assault on women with intent to outrage her modesty` | Numeric/integer-like | Count under the named head. | Matches same IPC women-related head. | Local equality measured; legal scope can vary by year/report. |
| `Insult to modesty of Women` | Numeric/integer-like | Count under the named head. | Matches IPC `INSULT TO MODESTY OF WOMEN`. | Local equality measured. |
| `Cruelty by Husband or his Relatives` | Numeric/integer-like | Count under named head. | Matches IPC `CRUELTY BY HUSBAND OR HIS RELATIVES`. | Local equality measured. |
| `Importation of Girls` | Numeric/integer-like | Count under named head. | Matches IPC `IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES`. | Local equality measured. |

For numeric fields, source tables describe figures as numbers; treat them as reported count measures, not rates. Exact incidence/case definitions require the NCRB annual table notes. The 2013–2014 values are not yet matched to official district source files.

## `ml-model/dataset/raw/CrimesOnWomenData.csv`

| Original column | Observed type | Meaning / unit / role | Cross-file relationship | Status |
|---|---|---|---|---|
| blank first header | Numeric-looking | Sequential/index-like field, likely export index. | Do not treat as geography, year, or crime measure. | Likely export artifact; unverified. |
| `State` | Text/category | State/UT text label. | State-level geography; no stable code. 33 casing-only state-label groups measured. | Header-derived. |
| `Year` | Numeric/integer-like | Annual period 2001–2021. | Time dimension. | Verified from values. |
| `Rape` | Numeric/integer-like | Presumed count for rape. | Possible counterpart to both district files. | Expansion from label; local source codebook absent. |
| `K&A` | Numeric/integer-like | Likely kidnapping and abduction. | Potentially corresponds to women/girls kidnapping measure. | Abbreviation expansion plausible, not verified by local documentation. |
| `DD` | Numeric/integer-like | Likely dowry deaths. | Potential counterpart to `Dowry Deaths`. | Abbreviation expansion plausible. |
| `AoW` | Numeric/integer-like | Likely assault on women with intent to outrage modesty. | Potential counterpart to corresponding women-crime measure. | Abbreviation expansion plausible. |
| `AoM` | Numeric/integer-like | Likely insult to modesty of women; some third-party copies expand it differently. | Potential counterpart to `Insult to modesty of Women`. | Ambiguous abbreviation; do not rename before source validation. |
| `DV` | Numeric/integer-like | Likely domestic violence/cruelty-related measure. | Could correspond to cruelty by husband/relatives, but definitions may not be equivalent. | Unverified; do not equate based on abbreviation. |
| `WT` | Numeric/integer-like | Likely women trafficking/importation of girls. | Possible counterpart to importation of girls, but concept and law scope may differ. | Unverified. |

All measures appear as integer-like aggregates; the local file has no codebook, unit note, or source attribution. Do not use a third-party abbreviation expansion as authoritative.

## `ml-model/dataset/synthetic/india_district_crime_2014_2023_30k.csv`

| Original column | Observed type | Meaning / unit / role | Status |
|---|---|---|---|
| `State` | Text/category | Generated state label, 12 distinct values. | Meaning is based on header; generator absent. |
| `District` | Text/category | Generated district label, 300 distinct values. | No authoritative geographic identity verified. |
| `Year` | Numeric/integer-like | Generated annual label, 2014–2023. | Generator absent. |
| `Crime_Type` | Text/category | 10 labels: Assault, Burglary, Cybercrime, Dowry Deaths, Fraud, Kidnapping, Murder, Rape, Robbery, Theft. | Generated category vocabulary; no mapping to NCRB definitions. |
| `Cases_Reported` | Numeric/integer-like | Presumed generated reported-case count. | Unverified semantics. |
| `Chargesheeted` | Numeric/integer-like | Presumed generated chargesheet count. | Unverified; not necessarily cohort-aligned to cases reported. |
| `Convictions` | Numeric/integer-like | Presumed generated conviction count. | Unverified; no cohort/period definition. |
| `Population` | Numeric/integer-like | Population denominator-like field. | No reference year, population source, or district linkage documented. |
| `Crime_Rate_per_100k` | Numeric/decimal | Rate field; arithmetically equals `Cases_Reported / Population × 100,000`, rounded to two decimals in all rows. | Formula measured; values and population provenance unverified. Derived from another field, so potential target leakage. |

## Cross-dataset category mapping cautions

- The strongest local measure mapping is between the seven women-specific district columns and corresponding IPC columns for 2001–2012; every one of 9,016 state/district/year keys matches after the diagnostic Delhi label alias.
- The IPC broad `KIDNAPPING & ABDUCTION` field is **not** equivalent to the women-specific field; the matching field is `KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS`.
- `AoM`, `DV`, and `WT` in the state-year file are ambiguous until a source data dictionary is located. Do not confidently map them to another dataset from acronym alone.
- Total fields and component/subcategory fields must not be summed without NCRB glossary definitions.
- Crime classification and law changed over the period. A same-looking label does not guarantee constant inclusion criteria across years.

[^2013]: [OGD India, Crime against Women during 2013](https://www.data.gov.in/resource/crime-against-women-during-2013).
[^ipc]: [OGD India, District-wise crimes under various sections of IPC crimes](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes).
