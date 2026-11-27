# SafeHer Official Source Artifact Reconciliation

**Review date:** 2026-11-28  
**Scope:** read-only comparison of the two user-provided files in `ml-model/source-verification/official-downloads/` with the matching existing repository CSVs. No source file was edited, renamed, moved, cleaned, or replaced. No preprocessing or model work was performed.

## Executive result

- Both downloaded files were identified confidently by filename, headers, and reporting period.
- `crcCAW_2013.csv` is **byte-identical** to the existing local 2013 file.
- `dstrIPC_1.csv` is **not byte-identical** to the existing local IPC file. All 9,017 records match as a multiset across all 33 named fields, including duplicate-row multiplicities. The existing local file has a blank 34th field (a trailing comma on every line) and a different row order. No missing/additional/different named-field records were found by this comparison.
- Both candidates remain **blocked pending verification** for preprocessing because exact resource-level license applicability was not established from the available metadata. The user must approve preprocessing separately.

## File identification and integrity

Counts below are CSV data rows excluding the header. All four files are valid UTF-8 without a BOM; all records have a consistent width within each file. They use CRLF line endings.

| Role | Filename | Size (bytes) | SHA-256 | Data rows × columns | Encoding |
|---|---|---:|---|---:|---|
| Official IPC download | `ml-model/source-verification/official-downloads/dstrIPC_1.csv` | 1,019,080 | `590BD77D0C827D68C4370F8FF94B126951ECBF1BD61D5E7DBB6DB9FDFB9A6388` | 9,017 × 33 | UTF-8, no BOM |
| Existing IPC source | `ml-model/dataset/raw/01_District_wise_crimes_committed_IPC_2001_2012.csv` | 1,028,098 | `7D789D9A1E9F539DBB757027BFADEFC4DA08E3D7C2E492750B421492298A5E65` | 9,017 × 34 | UTF-8, no BOM |
| Official 2013 download | `ml-model/source-verification/official-downloads/crcCAW_2013.csv` | 20,575 | `5D7AE9CA4E9179B7489FBB7BB7755DD59428204BABB5DDE1D881E8FF04BBCB99` | 456 × 3 | UTF-8, no BOM |
| Existing 2013 source | `ml-model/dataset/optional/crcCAW_2013.csv` | 20,575 | `5D7AE9CA4E9179B7489FBB7BB7755DD59428204BABB5DDE1D881E8FF04BBCB99` | 456 × 3 | UTF-8, no BOM |

Hashes were calculated with SHA-256 over the original file bytes. File sizes were measured from the filesystem. Inspection used Python's standard-library CSV reader; no project dataset was imported into a transformation pipeline.

### Header and structure comparison

**Official and local IPC common 33 headers, in order:**

```text
STATE/UT, DISTRICT, YEAR, MURDER, ATTEMPT TO MURDER,
CULPABLE HOMICIDE NOT AMOUNTING TO MURDER, RAPE, CUSTODIAL RAPE,
OTHER RAPE, KIDNAPPING & ABDUCTION,
KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS,
KIDNAPPING AND ABDUCTION OF OTHERS, DACOITY,
PREPARATION AND ASSEMBLY FOR DACOITY, ROBBERY, BURGLARY, THEFT,
AUTO THEFT, OTHER THEFT, RIOTS, CRIMINAL BREACH OF TRUST, CHEATING,
COUNTERFIETING, ARSON, HURT/GREVIOUS HURT, DOWRY DEATHS,
ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY,
INSULT TO MODESTY OF WOMEN, CRUELTY BY HUSBAND OR HIS RELATIVES,
IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES,
CAUSING DEATH BY NEGLIGENCE, OTHER IPC CRIMES, TOTAL IPC CRIMES
```

The existing local IPC CSV appends an empty 34th header and an empty 34th field to every data row. The official CSV does not. Both have 9,018 CRLF-terminated lines including the header; every local line ends with a comma and no official line does. The byte-size difference is exactly 9,018 bytes, matching one extra comma per line.

The IPC files' row order differs. Positional row comparison is therefore not appropriate. Comparison of the full records as an unordered multiset over the 33 official fields found identical multiplicities: **0 official records absent from local and 0 local records absent from official**. This preserves repeated records in the comparison and does not remove or resolve the RAILWAYS duplicate.

**Both 2013 headers, in order:** `State/UTs`, `Crime Head`, `2013`. Both have 456 data rows, width 3 for every record, same encoding, size, and SHA-256; therefore the files are byte-identical.

## Official source metadata

| Item | IPC district dataset | Crime against Women 2013 |
|---|---|---|
| Official source page | [OGD IPC district crime catalog](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes). The 2001–2012 resource is a catalog item; a separate item permalink was not established, so none is guessed here. | [OGD resource page](https://www.data.gov.in/resource/crime-against-women-during-2013); also in the [Crime against Women catalog](https://data.gov.in/catalog/crime-against-women). |
| Resource title | **District-wise crime under various sections of Indian Penal Code (IPC) crimes during 2001–2012** | **Crime against Women during 2013** |
| Publisher/contributor | NCRB, Ministry of Home Affairs / Department of States, per OGD catalog | NCRB, Ministry of Home Affairs / Department of States, per OGD resource/catalog |
| Reporting period | Annual 2001–2012; figures in numbers | Annual 2013; figures in numbers; source is *Crime in India 2013* |
| Publication/update | OGD catalog: 17/09/2013; updated 17/04/2014 | OGD resource page: 10/12/2014; updated 10/12/2014 |
| OGD size shown | 995 KB, rounded portal value | 20 KB, rounded portal value |
| Retrieval date | Not independently known. Windows file `LastWriteTime` observed as 2026-11-28 00:30:30; not proven to be download time. | Not independently known. Windows file `LastWriteTime` observed as 2026-11-28 00:33:16; not proven to be download time. |

The official catalog provides an IPC district/special-police reporting note for later-year resources; it does not by itself explain every unit in the 2001–2012 table or the duplicate. The 2013 resource's schema, period, source title, and local bytes match the OGD record. The file comparison confirms identity to the copy in the official-downloads folder, but cannot independently authenticate how that downloaded copy was obtained.

## License and attribution review

The IPC OGD catalog is visibly marked **Released Under: National Data Sharing and Accessibility Policy (NDSAP)**. The 2013 resource is listed in an OGD catalog that carries the same NDSAP designation. **NDSAP is a policy/release designation; it is not, on its own, the specific license text.**

OGD [Terms of Use](https://www.data.gov.in/terms-of-use) state that catalog/resource terms are set by the `license` metadata element of each dataset record, except where otherwise noted. The OGD site notice broadly says portal content is licensed under [Government Open Data License–India](https://data.gov.in/Godl); GODL-India requires provider/source/license attribution and imposes conditions including non-endorsement and scope/exemptions. The source CSVs themselves contain no embedded license notice. The reviewed record/catalog views did not expose a clearly populated item-specific license value tying the precise downloaded version to GODL-India.

**License decision:** the portal-level GODL notice is evidence of the platform's general licensing framework, but the exact resource-level license applicability to the official downloads/local copies has not been conclusively captured. License is **not cleared** for this project checkpoint. If the record-specific license confirms GODL-India coverage, use the GODL attribution format with verified provider, title, repository/version/publication date, URL, and license URL. Do not present the conditional attribution template in the provenance manifest as completed until this check is done.

## Duplicate and aggregate preservation

The IPC local file contains the already documented two non-identical `JAMMU & KASHMIR / RAILWAYS / 2010` records. They are present in both file versions with the same multiplicity; the official download does not resolve their meaning. Preserve both records, their source row identities, and the existing source file. Flag the shared natural key as unresolved and quarantine it from analyses requiring a unique geography. Do not delete, merge, average, or assign either record to a revenue district without authoritative evidence. Keep all total/subtotal rows separately classified; this file comparison does not authorize any aggregate operations.

## Final readiness decisions

| Dataset | Decision | Reason |
|---|---|---|
| IPC district 2001–2012 | **Blocked pending verification** | Source-content match is verified as an unordered multiset and formatting/order difference is explained. Still blocked on record-level license applicability and user approval; RAILWAYS, special reporting units, and aggregates need explicit exclusions/classification. |
| Crime against Women 2013 | **Blocked pending verification** | Byte-identical official download/local copy and strong OGD source record match. Still blocked on record-level license applicability and user approval; totals and IPC/SLL category handling need explicit treatment. |
| Women district 2001–2014 compilation | **Blocked pending verification** | No official artifact reconciliation or dataset-level license resolution was performed for it. |
| `CrimesOnWomenData.csv` 2001–2021 | **Blocked pending verification** | No official artifact reconciliation, publisher/version, license, or category-definition resolution was performed for it. |
| Synthetic district 2014–2023 file | **Testing only** | No new source evidence; existing synthetic-only restriction remains. |

No dataset is approved for supplementary descriptive preprocessing at this stage. The two OGD/NCRB files are the candidates closest to readiness, but license verification and explicit user approval remain necessary. No Phase 2D preprocessing began.

## Files and commands/evidence

- Updated `docs/data-provenance-manifest.md` with official filenames, hashes, sizes, schema comparison, source record fields, license caveat, and observed filesystem timestamps.
- Updated `docs/preprocessing-readiness-checklist.md` with completed identification/integrity checks and unresolved license/retrieval-date gates.
- Created this report.
- Official source URLs are listed above; prior source and methodology evidence remains in [`dataset-verification-report.md`](dataset-verification-report.md) and [`dataset-eligibility-matrix.md`](dataset-eligibility-matrix.md).

Read-only commands/operations used: PowerShell `Get-ChildItem`, `Get-Item`, `Get-FileHash -Algorithm SHA256`; Python standard-library byte reads, UTF-8 validation, `csv.reader`, header/row-width counts, positional comparison, and unordered full-record multiset comparison. No source was downloaded by the inspection process, and no dependency was installed.

## References

- OGD/NCRB [IPC district crime catalog](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes).
- OGD/NCRB [Crime against Women during 2013 resource](https://www.data.gov.in/resource/crime-against-women-during-2013).
- OGD [Terms of Use](https://www.data.gov.in/terms-of-use) and [Government Open Data License–India](https://data.gov.in/Godl).
- NCRB [Crime in India 2012 table contents](https://www.ncrb.mha.gov.in/crime-in-india-table-content?year=2012).
