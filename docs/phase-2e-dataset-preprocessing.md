# SafeHer Phase 2E: Actual Dataset Preprocessing

**Status: Partially blocked. No research dataset was read or transformed.**

## Scope and decision

The approved scope was to prepare independent supplementary descriptive outputs for the IPC 2001–2012 and Crime against Women 2013 datasets. The authorization from the project supervisor/user is recorded for this phase. It does not establish the publisher's license terms.

The OGD Terms of Use state that dataset/resource terms are described in the `license` metadata element of the individual dataset record, except where otherwise noted. The repository's [data provenance manifest](data-provenance-manifest.md) records that this item-level metadata was not captured for either candidate. The 2013 OGD resource page was checked again during Phase 2E; the available page view displayed the general site notice but no populated item-level license field. The IPC catalog item likewise has no captured resource-level license value. NDSAP designation and a portal-wide GODL notice do not, on their own, resolve the applicability of a specific license to these local artifacts.

**License gate: not cleared for either dataset.** In accordance with the phase instructions, neither candidate was supplied to the preprocessing pipeline. No source CSV or official download was opened, parsed, hashed, or transformed during this phase.

## Candidate decisions

| Dataset | Existing source evidence | License gate | Phase 2E result |
|---|---|---|---|
| IPC district crimes, 2001–2012 | Official download identified as `dstrIPC_1.csv`; 9,017 source records match the local file as an unordered multiset across the 33 named columns. The local file has a trailing empty field and different order. Details and prior hashes are in the provenance manifest. | **Unresolved**; no record-level license applicability established. | **Blocked; not processed.** No input/output hashes or preprocessing counts generated. |
| Crime against Women, 2013 | Official download identified as `crcCAW_2013.csv`; existing local copy was previously verified byte-identical. Details and prior hashes are in the provenance manifest. | **Unresolved**; no record-level license applicability established. | **Blocked; not processed.** No input/output hashes or preprocessing counts generated. |
| District compilation, 2001–2014 | Remains quarantined under prior provenance/readiness review. | Not reviewed for this phase. | Not processed. |
| `CrimesOnWomenData.csv` | Remains quarantined under prior provenance/readiness review. | Not reviewed for this phase. | Not processed. |
| Synthetic 2014–2023 data | Existing project file remains testing-only; it was not used as observed data in this phase. | Not applicable to observed-source eligibility. | Not processed. |

## Transformations and outputs

No transformations were performed. No accepted, flagged, or quarantined research records were produced. No Phase 2E dataset output or quality report was generated. Therefore there are no Phase 2E input/output hash pairs, row counts, or dataset-specific validation results to report. Original row counts and hashes remain as previously documented in the inspection and provenance documents; they were not re-measured for this phase.

The existing generic preprocessing implementation was reviewed. It supports configured type checks, flags, quarantine, count conservation, and new-file-only output. However, source-specific rules for all aggregate classifications, twelve-total reconciliation in the 2013 file, and reliable preservation of source row ordinals need a synthetic-only test/config review before future use. This review does not authorize a run against either actual candidate.

## RAILWAYS, aggregates, and categories

The two `JAMMU & KASHMIR / RAILWAYS / 2010` rows were not read in this phase. The previously approved preservation policy remains: retain both records and their source identities, flag the unresolved reporting unit, and quarantine them from unique-geography analyses. Never delete, merge, average, or silently correct either row.

No aggregate or subtotal rows were changed. If the license gate is cleared later, the IPC trailing empty field may be omitted from a derived output only through an explicit logged transformation; source fields and original values must remain auditable. For the 2013 dataset, preserve IPC and SLL categories separately and keep State, UT, and All-India totals separate from their detail rows. Do not infer category or geography mappings.

## Testing and validation

The existing synthetic-only suite was run with the repository virtual environment:

```powershell
cd ml-model
$env:PYTHONDONTWRITEBYTECODE = '1'
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Result: **16 tests passed**. They exercised the existing artificial fixture, count preservation/quarantine, duplicate and aggregate flags, validation, CLI behavior, and report writing. These results verify the current generic pipeline against artificial test data only; they do not validate either candidate dataset or clear its license gate.

No additional transformations or tests were added in this phase because actual-data work is blocked and the existing suite already exercises only artificial fixtures. No Python packages were installed. No model training, EDA, frontend/backend changes, database access, or `.env` access occurred.

## Attribution and remaining conditions

No final attribution statement is asserted. The exact item-level license, its applicability to the downloaded/local artifact, and any resulting required attribution remain unverified. General OGD Terms of Use say to rely on each record's license metadata; obtain and preserve that record-level evidence (or written clarification from the publisher) before proceeding. If GODL-India coverage is confirmed, record the exact source/provider/title/version/date/URL and required attribution/non-endorsement terms rather than using an incomplete template.

Before retrying Phase 2E:

1. Capture authoritative item-level license metadata for both resources, or obtain written publisher clarification that identifies the resources and applicable terms.
2. Update and review the provenance manifest and attribution text.
3. Confirm source artifact lineage, including the IPC row-order/trailing-field difference.
4. Complete synthetic-only tests for the source-specific aggregate handling, 2013 twelve-total reconciliation, IPC RAILWAYS row-ordinal quarantine, and output lineage.
5. Review proposed dataset-specific configs and output paths; preserve raw inputs and refuse overwrites.
6. Reconfirm the narrowly scoped preprocessing authorization after the license evidence is available.

## References

- OGD [Terms of Use](https://www.data.gov.in/terms-of-use), which states that individual resource `license` metadata governs except where otherwise noted.
- OGD [Crime against Women during 2013 resource](https://www.data.gov.in/resource/crime-against-women-during-2013); the page view available during this phase did not expose a populated item-level license field.
- OGD/NCRB [IPC crimes catalog](https://www.data.gov.in/catalog/district-wise-crimes-under-various-sections-indian-penal-code-ipc-crimes); its item-level license remains uncaptured in the repository evidence.
- OGD [Government Open Data License–India](https://data.gov.in/Godl), cited as conditional only; applicability to either candidate has not been established.
