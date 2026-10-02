# Canonical Samhita Content Contract v1

## Purpose

Every future AaptaKosha Samhita chapter MUST expose the same logical contract, regardless of how the source files are packaged.

`Samhita → Sthana → Adhyaya → Verse` is the canonical address hierarchy.

### Required chapter shape

- **Samhita**: stable text identity and title.
- **Sthana**: stable section identity/number/title.
- **Adhyaya**: stable chapter identity/number/title and expected verse count.
- **Verse**: the atomic canonical learning record.

Each verse may carry:
- canonical Sanskrit
- verse number
- Hindi translation
- explanation
- टीका mapping/summary
- learning-unit references
- assessment references
- revision references
- source references

Chapter-level collections provide:
- learning units
- assessments
- revision references
- source metadata
- quality gates

## Non-negotiable rules

1. **Stable IDs:** IDs are permanent API/content identifiers; filenames are not identifiers.
2. **One canonical Sanskrit field:** the canonical Sanskrit text lives on the verse record. Do not maintain a second competing Sanskrit copy.
3. **Verse addressing:** every verse has a unique `verse_id` and integer `verse_no`.
4. **References, not duplication:** learning, assessment and revision objects reference verse IDs/content IDs rather than copying canonical Sanskrit.
5. **Source provenance:** every verse must point to at least one source metadata record.
6. **Translation separation:** Hindi translation is an AaptaKosha learning layer and must remain distinct from source commentary.
7. **Commentary integrity:** published commentary may be mapped/attributed; unavailable or unverified commentary must never be fabricated.
8. **Learning units are ranges/sets:** a unit references verses and may define objectives and study explanation.
9. **Assessment is content-linked:** every assessment item declares the content references it tests.
10. **Revision is addressable:** revision cards/questions must be linkable back to verse or learning-unit IDs.
11. **Source metadata is explicit:** source role (canonical text, cross-check, commentary, curriculum, etc.) is stored rather than inferred.
12. **No bespoke chapter schema:** new texts may have different storage adapters, but their published API payload MUST conform to this contract.
13. **Partial chapters are explicit:** missing layers are represented by absent optional fields plus quality-gate status; they must not be silently presented as complete.
14. **Publication gate:** a chapter cannot be considered complete merely because Sanskrit exists. Source verification and all required learning layers must pass the project quality gate.

## Canonical ID examples

- `charaka.sutra.01`
- `charaka.sutra.01.001`
- `sarangadhara.purva.01`
- `sarangadhara.purva.01.001`

The same pattern applies to Ashtanga Hridaya, Madhava Nidana and future texts.

## Storage policy

Existing chapter packages do not need to be rewritten in one risky batch. Adapters may read legacy packages and emit this canonical representation. New content must be authored directly against v1.

The JSON Schema is authoritative for shape; semantic validation is additionally required for sequence, reference resolution and quality gates.
