# Charaka Sūtrasthāna 9 — Research Manifest

## Scope
- Curriculum: `AyUG-SA1` / First Professional.
- Classical identity: Caraka Saṃhitā, Sūtrasthāna 9.
- Title: **Khuḍḍākacatuṣpāda** (खुड्डाकचतुष्पाद).
- Primary Sanskrit sequence: Vedic Samhita, Caraka Sūtrasthāna 9.
- Source URL: https://www.vedicsamhita.in/ayurveda/caraka/1/9
- Underlying edition identified by the source page: SARIT `carakasamhita.xml`.
- Source reports **55 passages, 3 in prose**.
- The source explicitly states that its Devanagari is mechanically transliterated from SARIT IAST and that no English translation is included.

## Canonical sequence contract
Preserve SARIT/Vedic Samhita passage references exactly; do not silently renumber prose or half-verses.

Expected source structure:
- 9.1 — prose
- 9.2 — prose
- 9.3ab–9.26cd — 48 verse-half passages
- 9.27 — prose heading: `तत्र श्लोकौ`
- 9.27ab–9.28cd — 4 concluding verse-half passages
- Total: **55 passages = 3 prose + 52 verse-half passages**.

Canonical implementation should therefore retain prose passages separately from verse-half passages, with stable passage IDs such as `charaka.sutra.09.003ab` and `charaka.sutra.09.027`.

## Primary-source thematic map
1. 9.1–9.2 — chapter opening and Atreya attribution.
2. 9.3–9.5 — the four therapeutic limbs (pāda-catuṣṭaya), health/disease, and the aim of treatment.
3. 9.6 — four qualities of the physician: learning, extensive practical experience, skill, and cleanliness.
4. 9.7 — four qualities of therapeutic substances/dravyas.
5. 9.8 — four qualities of the attendant/paricāraka.
6. 9.9 — qualities of the patient/ātura.
7. 9.10–9.13 — sixteenfold causal structure, physician's primacy, and the necessity of the physician alongside the other three limbs.
8. 9.14–9.18 — danger of severe disease, risks of an unqualified physician, and the physician as `prāṇābhisara` when properly grounded.
9. 9.19–9.20 — fourfold clinical knowledge and contextual discernment in treatment.
10. 9.21–9.24 — six qualities supporting the physician, the elements associated with the word “vaidya”, and the relationship of śāstra, buddhi and clinical action.
11. 9.25–9.26 — physician responsibility, self-development, and the fourfold professional disposition.
12. 9.27–9.28 — concluding summary of the four limbs and the physician's primacy.

## Content-generation rules
- Retain the Sanskrit original separately from Hindi translation.
- Translate each passage specifically; do not merge adjacent half-verses into an untraceable block.
- Every passage must receive passage-specific Hindi explanation and passage-specific टीका.
- Historical/professional terminology should be explained in context rather than silently modernized.
- Assessment questions must reference only canonical passage IDs.
- Do not infer NCISM recitation status unless an authoritative curriculum/source mapping explicitly establishes it.
- Chapter 13 onward remains outside this SA-1 pipeline and is reserved for SA-2 / Second Professional.

## Integration gate
After canonical content:
1. 20-question revision assessment with canonical refs.
2. Static regression for counts, sequence, Sanskrit/translation/explanation/टीका uniqueness, and assessment refs.
3. Reader/API wiring.
4. End-to-end learner regression when execution environment permits.
