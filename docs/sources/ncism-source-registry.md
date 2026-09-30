# NCISM Source Registry

**Registry version:** 0.1.1  
**Last verified:** 2026-09-30  
**Status:** Phase 0 baseline frozen

This registry is the canonical starting list for NCISM curriculum and regulatory references used by AaptaKosha.

| Source ID | Authority | Scope | Canonical entry point | Verification |
|---|---|---|---|---|
| SRC-NCISM-UG | NCISM | BAMS undergraduate curriculum index | https://www.ncismindia.org/ayurveda-syllabus.php | 2026-09-30 |
| SRC-NCISM-I | NCISM | 1st Professional BAMS | https://www.ncismindia.org/I-year-syllabus.php | 2026-09-30 |
| SRC-NCISM-II | NCISM | 2nd Professional BAMS | https://www.ncismindia.org/II%20year%20syllabus.php | 2026-09-30 |
| SRC-NCISM-III | NCISM | 3rd Professional BAMS | https://www.ncismindia.org/IIIrd-prof-BAMS.php | 2026-09-30 |
| SRC-NCISM-IV | NCISM | 4th Professional BAMS | Covered by the official BAMS curriculum index; dedicated endpoint to be captured when exposed by NCISM | 2026-09-30 |
| SRC-NCISM-REG | NCISM | Regulatory framework under NCISM Act 2020 | https://www.ncismindia.org/under-ncism-act-2020.php | 2026-09-30 |

## Verification evidence

The official NCISM BAMS curriculum index explicitly lists 1st, 2nd, 3rd, and 4th Professional BAMS curriculum sections. The first-professional page currently exposes the First Professional curriculum collection, while NCISM-published curriculum documents demonstrate version/effective-date metadata and may include corrections or implementation updates.

The registry therefore freezes the official index and professional-year entry points as the Phase 0 source baseline. Individual curriculum documents remain versioned source artifacts and must be captured separately during Phase 1 ingestion.

## Registry rules

1. Prefer official NCISM sources over secondary copies.
2. Record document/version/effective-scope metadata whenever available.
3. Do not silently overwrite an older authoritative record; mark supersession explicitly.
4. Curriculum-derived records must retain a provenance link to the source entry and source artifact.
5. Re-verification must record the verification date even when the source URL is unchanged.
6. A source entry is not itself the curriculum content; linked documents are independently versioned artifacts.
7. New NCISM corrections, transitional curricula, or replacement documents must create new source/artifact records rather than rewriting historical records.

This registry is frozen as the Phase 0 source-entry baseline. Expanding the registry with individual subject PDFs, correction notices, implementation guidance, academic calendars, and other operational sources is a Phase 1 ingestion task.
