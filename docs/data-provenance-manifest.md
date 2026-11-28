# SafeHer Data Provenance Manifest

**Manifest prepared:** 2026-11-28  
**Scope:** the two OGD/NCRB candidate files considered for supplementary descriptive preprocessing. This is a local evidence record, not a legal determination or proof that local files are byte-identical to publisher files. Original CSVs were read only for filesystem size/hash; neither was altered.

## Source and local artifact records

| Field | IPC district 2001–2012 | Crime against Women 2013 |
|---|---|---|
| Exact local filename | `ml-model/dataset/raw/01_District_wise_crimes_committed_IPC_2001_2012.csv` | `ml-model/dataset/optional/crcCAW_2013.csv` |
| Official OGD URL checked | [OGD catalog: District-wise crimes under various sections of IPC](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes) | [OGD resource: Crime against Women during 2013](https://www.data.gov.in/resource/crime-against-women-during-2013); also listed in [OGD Crime against Women catalog](https://data.gov.in/catalog/crime-against-women) |
| Resource title | Catalog lists **District-wise crime under various sections of Indian Penal Code (IPC) crimes during 2001–2012**. A separate resource URL for that specific catalog item was not located during this review; do not invent one. | **Crime against Women during 2013** |
| Publisher/contributor | NCRB (National Crime Records Bureau), Ministry of Home Affairs / Department of States, as shown on OGD catalog | NCRB (National Crime Records Bureau), Ministry of Home Affairs / Department of States, as shown on OGD resource/catalog |
| Reporting period and frequency | 2001–2012; annual; figures in numbers | 2013; annual; figures in numbers |
| Official page publication/update metadata | Catalog-level dates: published 17/09/2013; updated 17/04/2014 | Resource page: published 10/12/2014; updated 10/12/2014 |
| OGD release/license evidence visible | Catalog says **Released Under: National Data Sharing and Accessibility Policy (NDSAP)**. The item-specific license metadata was not available in the page view retrieved. | Parent catalog says released under NDSAP. Individual resource page does not expose a specific license field in the retrieved metadata. |
| License status for this local artifact | **Not verified.** Do not infer that this local byte sequence is covered by GODL-India solely from the catalog/NDSAP label. | **Not verified.** Strong structural source match does not establish item-level licensing or exact local artifact identity. |
| Attribution requirement evidence | OGD terms state individual dataset license metadata governs; OGD/GODL-India pages state provider/source/license attribution for covered data. Exact binding license for this local artifact is unverified. | Same limitation; if the item-level record confirms GODL-India coverage, attribute NCRB/provider, resource title, OGD, publication/version date, resource URL, and license URL. |
| Local size | 1,028,098 bytes (measured locally) | 20,575 bytes (measured locally) |
| Local SHA-256 | `7D789D9A1E9F539DBB757027BFADEFC4DA08E3D7C2E492750B421492298A5E65` | `5D7AE9CA4E9179B7489FBB7BB7755DD59428204BABB5DDE1D881E8FF04BBCB99` |
| Retrieval date of local copy | **Unknown / not recorded.** No reliable source retrieval timestamp was found. Manifest preparation date is not the data retrieval date. | **Unknown / not recorded.** No reliable source retrieval timestamp was found. Manifest preparation date is not the data retrieval date. |
| Source/local checksum comparison | See “Official artifact reconciliation” below: non-identical hashes, but all records match as an unordered multiset across 33 named columns; local has an extra blank trailing field and different row order. | See “Official artifact reconciliation” below: official download and local file are byte-identical. |
| Source evidence judgment | **Official content match verified at record-multiset level; byte-level identity differs due row order and empty trailing field.** | **Byte-level identity with the user-provided official download verified; source acquisition itself is not independently authenticated.** |

## Verified facts versus unknowns

### Verified in official source records

- The OGD catalog identifies NCRB as contributor to its IPC district-crime catalog and lists the annual 2001–2012 resource, publication/update dates, and a rounded 995 KB file-size label. The catalog describes numbers and, for later editions, explicitly warns that district reporting includes police districts and special police units rather than necessarily matching revenue districts.
- The OGD resource page identifies the 2013 resource title, NCRB/MHA publisher path, annual granularity, fields `State/UTs`, `Crime Head`, `2013`, figures in numbers, source *Crime in India 2013*, and a rounded 20 KB size.
- OGD terms state that dataset-record license metadata governs. GODL-India describes reuse conditions and a required attribution statement for data covered by that license.

### Not verified; do not fill by assumption

- Whether the user-provided official downloads were themselves altered before entering the official-downloads folder; hash comparison only establishes their present bytes and match relationship to local copies.
- The IPC 2001–2012 catalog item's distinct resource URL, if one exists separately from the catalog URL.
- Item-level license metadata / definitive GODL-India coverage for the two exact local byte sequences.
- Retrieval dates of the local files.
- Any legal conclusion about redistribution or derivative use.

## Attribution template if record-level GODL coverage is confirmed

Use the OGD template with verified values only, for example:

> National Crime Records Bureau, [verified publication year], [verified resource title], Open Government Data Platform India, [verified version/publication date], [verified resource URL]. Published under Government Open Data License–India: https://data.gov.in/Godl.

Do not publish this example as a completed attribution until its bracketed metadata and resource-level license are verified.

## Integrity and handling

- SHA-256 values above were calculated from the existing local files using PowerShell `Get-FileHash -Algorithm SHA256`; sizes were measured with `Get-Item`.
- Hashes identify the current local bytes only. They do not authenticate a publisher source or prove immutability over time unless recomputed and compared later.
- No source CSV has been modified. Preserve the original files read-only and store any future processed outputs separately with their own lineage and hashes.

## Official references

- OGD/NCRB [IPC crimes catalog](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes).
- OGD/NCRB [Crime against Women during 2013 resource](https://www.data.gov.in/resource/crime-against-women-during-2013) and [Crime against Women catalog](https://data.gov.in/catalog/crime-against-women).
- OGD [Terms of Use](https://www.data.gov.in/terms-of-use) and [Government Open Data License–India](https://data.gov.in/Godl).
- NCRB [Crime in India 2012 table contents](https://www.ncrb.mha.gov.in/crime-in-india-table-content?year=2012).

## Official artifact reconciliation (2026-11-28)

The two files in `ml-model/source-verification/official-downloads/` were identified by filename, headers, and period. For both, SHA-256, byte size, CSV rows, headers, and UTF-8 validity were checked. No file was written during this comparison. This addendum supersedes the earlier “not performed” comparison statements above.

| Field | IPC 2001–2012 | Crime against Women 2013 |
|---|---|---|
| Official downloaded filename | `dstrIPC_1.csv` | `crcCAW_2013.csv` |
| Corresponding local filename | `ml-model/dataset/raw/01_District_wise_crimes_committed_IPC_2001_2012.csv` | `ml-model/dataset/optional/crcCAW_2013.csv` |
| Download directory | `ml-model/source-verification/official-downloads/` | `ml-model/source-verification/official-downloads/` |
| Official downloaded bytes | 1,019,080 | 20,575 |
| Official downloaded SHA-256 | `590BD77D0C827D68C4370F8FF94B126951ECBF1BD61D5E7DBB6DB9FDFB9A6388` | `5D7AE9CA4E9179B7489FBB7BB7755DD59428204BABB5DDE1D881E8FF04BBCB99` |
| Official downloaded rows × columns | 9,017 × 33 (header excluded from row count) | 456 × 3 (header excluded from row count) |
| Headers | `STATE/UT`, `DISTRICT`, `YEAR`, `MURDER`, `ATTEMPT TO MURDER`, `CULPABLE HOMICIDE NOT AMOUNTING TO MURDER`, `RAPE`, `CUSTODIAL RAPE`, `OTHER RAPE`, `KIDNAPPING & ABDUCTION`, `KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS`, `KIDNAPPING AND ABDUCTION OF OTHERS`, `DACOITY`, `PREPARATION AND ASSEMBLY FOR DACOITY`, `ROBBERY`, `BURGLARY`, `THEFT`, `AUTO THEFT`, `OTHER THEFT`, `RIOTS`, `CRIMINAL BREACH OF TRUST`, `CHEATING`, `COUNTERFIETING`, `ARSON`, `HURT/GREVIOUS HURT`, `DOWRY DEATHS`, `ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY`, `INSULT TO MODESTY OF WOMEN`, `CRUELTY BY HUSBAND OR HIS RELATIVES`, `IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES`, `CAUSING DEATH BY NEGLIGENCE`, `OTHER IPC CRIMES`, `TOTAL IPC CRIMES` | `State/UTs`, `Crime Head`, `2013` |
| Encoding | Valid UTF-8, no BOM; 9,018 CRLF-terminated lines | Valid UTF-8, no BOM; 457 CRLF-terminated lines |
| Existing local bytes / SHA-256 | 1,028,098 / `7D789D9A1E9F539DBB757027BFADEFC4DA08E3D7C2E492750B421492298A5E65` | 20,575 / `5D7AE9CA4E9179B7489FBB7BB7755DD59428204BABB5DDE1D881E8FF04BBCB99` |
| Hash result | **Not byte-identical.** | **Byte-identical.** |
| Record comparison | All 9,017 rows match as an unordered multiset across the 33 named fields, preserving multiplicity. The official file has 33 fields per row; the local file has the same first 33 fields plus a blank 34th field. All row order differs when compared positionally. | Exact file hash, byte size, row count, headers, and content match. |
| Explanation | The local CSV has a trailing comma (empty final field) on each of 9,018 lines, adding exactly 9,018 bytes, and the records are in a different order. No missing/additional/different named-field records were found by multiset comparison. | None needed; the existing local file is the exact same byte sequence as the downloaded copy. |
| Official file filesystem timestamp | PowerShell `LastWriteTime` observed as 2026-11-28 00:30:30 (local display). This is file metadata, not proven download time. | PowerShell `LastWriteTime` observed as 2026-11-28 00:33:16 (local display). This is file metadata, not proven download time. |
| Proven retrieval date | Unknown; local timestamp is not sufficient evidence. | Unknown; local timestamp is not sufficient evidence. |

### License evidence after downloading

- The OGD catalog record visibly labels the IPC catalog as **Released Under: NDSAP**. The 2013 resource appears in the OGD Crime against Women catalog, which also carries an NDSAP designation. This identifies policy designation, not by itself the text or scope of an individual license.
- The OGD [Terms of Use](https://www.data.gov.in/terms-of-use) say that catalog/resource terms are those in each record's `license` metadata element, except as otherwise noted. The [GODL-India](https://data.gov.in/Godl) document describes a license and attribution conditions; the OGD footer/site notice also states that published content is licensed under GODL-India.
- The official CSV files contain no license metadata, and the reviewed resource/catalog pages do not expose a clearly populated per-resource `license` field that ties the exact downloaded file/version to GODL-India. Therefore this review records **NDSAP designation: visible; resource-level license applicability to these exact downloaded artifacts: not conclusively verified**. Do not claim legal clearance.
- If record-level GODL-India applicability is confirmed, the attribution must identify the provider, source, resource, OGD repository/version/date, URL, and license URL; the GODL-India template also requires attribution and non-endorsement. Do not use the conditional template above as a final completed citation until the license field is captured.

### Source verification updates

- The downloaded 2013 file matches the official OGD resource page by URL/title and is byte-identical to the existing local file. This confirms local artifact identity relative to this downloaded file, not independent origin/authenticity of the download process.
- `dstrIPC_1.csv` is identified as the 2001–2012 IPC district resource by the expected 33 headers, annual period, and content matching the existing local file as an unordered record multiset. Its changed ordering and extra local blank field explain the hash/size difference. The OGD catalog reports a rounded 995 KB; do not use that display size as an exact byte checksum.
- The OGD catalog's item is shown within the official [IPC district-crime catalog](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes); a separate resource permalink for the 2001–2012 entry was not established. The 2013 item has its own [official resource URL](https://www.data.gov.in/resource/crime-against-women-during-2013).

### Readiness consequence

The source-content comparison is now resolved enough to identify both official downloads: the 2013 file is byte-identical, and the IPC file has an exact multiset match over named fields with an explained formatting/order difference. **Both remain blocked from preprocessing** pending explicit item-level license metadata/applicability review and user approval. The IPC file additionally requires the existing RAILWAYS quarantine, aggregate/special-unit exclusions, and a source-order/blank-column preservation decision for any derived output.

## Phase 2E license gate recheck (2026-11-28)

The supervisor/user approval for the Phase 2E scope has been received. This is project authorization and does not establish publisher license terms. The OGD Terms of Use were checked again and state that resource terms are described by the `license` metadata element of each individual dataset record, except where otherwise noted. The available OGD 2013 resource page view showed the general portal notice but no populated item-level license field; the IPC catalog record still has no captured item-level license value in the evidence package. NDSAP designation and the general portal GODL notice are not treated as proof of the applicable license for either exact downloaded artifact.

**Decision:** Both candidate licenses remain unresolved, so neither local candidate was read or transformed in Phase 2E. No preprocessing input/output hashes, accepted/quarantined counts, or dataset validation results were generated. The official source artifact hashes and prior structural comparisons above remain historical evidence from the earlier read-only reconciliation, not new Phase 2E measurements. See [Phase 2E dataset preprocessing](phase-2e-dataset-preprocessing.md) for scope, test result, and next gates.
