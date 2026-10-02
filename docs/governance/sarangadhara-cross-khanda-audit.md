# Śārṅgadhara Saṃhitā — Cross-Khaṇḍa Audit

Date: 2026-10-02

## Locked structure
- Pūrva Khaṇḍa: 7 chapters
- Madhyama Khaṇḍa: 12 chapters
- Uttara Khaṇḍa: 13 chapters
- Total: 32 chapters

## Audit result
All 32 chapter JSON packages are present in the repository and have an explicit chapter identity, verified verse extent, colophon, learning units, assessments and source-safety/anti-fabrication gates.

## Source-critical discrepancies preserved
- Pūrva Ch2: printed/online witness handling remains source-reconciled.
- Pūrva Ch6–7: complete chapter extents are locked, while non-anchor printed transcription remains a refinement task.
- Madhyama Ch10: online 1–92 vs printed Dīpikā 1–94.
- Madhyama Ch12: online 1–293 vs printed Dīpikā 1–295.
- Uttara Ch1: online 1–33 vs printed Dīpikā 1–35.
- Uttara Ch3: online gaps are preserved; printed witness reaches v36.
- Uttara Ch13: primary canonical v1–128 vs printed/editorial v129.

## Refinement policy
Anchor-level packages are not promoted to “full transcription” status without controlled source extraction. The next content refinement should prioritize chapters with the largest unresolved transcription gaps, while retaining exactly one consolidated commit per chapter.

## Runtime note
This audit is content-contract only. It does not trigger Vercel deployments and does not change application runtime schemas.
