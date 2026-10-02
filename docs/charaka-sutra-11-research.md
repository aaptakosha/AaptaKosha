# Charaka Sūtrasthāna 11 — Tisraiṣaṇīya: research manifest

- Curriculum: **AyUG-SA1 / First Professional**
- Classical identity: **Caraka Saṃhitā, Sūtrasthāna 11**
- Title: **Tisraiṣaṇīya (तिस्रैषणीय)**
- Primary sequence source: Vedic Samhita, Caraka Sūtrasthāna 11.
- Source page: https://www.vedicsamhita.in/ayurveda/caraka/1/11
- Underlying edition: SARIT IAST edition; Vedic Samhita states that its Devanagari is mechanically transliterated from that edition.
- Source reports **103 passages, 39 in prose**. citeturn0view0

## Canonical sequence contract

Preserve SARIT/Vedic Samhita passage labels exactly rather than collapsing prose and verse halves.

Verified structural landmarks:
- 11.1–11.8 are prose.
- 11.9 is prose, followed by 11.9ab–11.16cd verse-half passages.
- 11.17–11.18 are prose; 11.18ab–11.26cd are verse-half passages.
- 11.27–11.33 are prose.
- 11.34–11.49 are prose.
- 11.50 is prose, followed by 11.50ab–11.53cd verse-half passages.
- 11.54–11.56 are prose; 11.56ab–11.63cd are verse-half passages.
- 11.64 is prose; 11.64ab–11.65cd are concluding verse-half passages.

The page itself identifies 103 total passages and 39 prose passages; individual labels above are taken directly from the primary page. citeturn3view0turn2view0

**Important source-audit note:** the source page's aggregate count is authoritative for this content gate. Before canonical generation, reconcile the complete 103-label list against the fetched page so no passage is omitted or invented.

## Major thematic sequence

1. **11.1–11.8 — The three eṣaṇās**
   - Prāṇaiṣaṇā, dhanaiṣaṇā, paralokaiṣaṇā.
   - Preservation of life through healthy conduct and care of disease.
   - Wealth/resources and socially acceptable livelihood.
   - Debate concerning paraloka/punarbhava and the limits of perception.
   - The text's argument that perception alone does not exhaust valid knowledge.

2. **11.9–11.16 — Argument concerning punarbhava**
   - Questions raised against alternative explanations.
   - Classical reasoning about self, body, causation and karma.
   - These arguments must be taught as the **text's classical philosophical position**, not as a modern empirical claim.

3. **11.17–11.33 — Four pramāṇas and the third eṣaṇā**
   - Āptopadeśa, pratyakṣa, anumāna and yukti.
   - Characteristics and examples of reliable testimony.
   - Inference from observed signs and causal patterns.
   - Yukti as multi-factor reasoning.
   - The text applies these four pramāṇas to its discussion of punarbhava and dharma.

4. **11.34–11.44 — Three upastambhas, bala and hetu**
   - Three supports: āhāra, svapna, brahmacarya.
   - Three forms of bala: sahaja, kālaja, yuktikṛta.
   - Three āyatana and their ati-yoga, ayoga and mithyā-yoga.
   - Indriya-artha interaction and bodily, verbal and mental action.
   - Prajñāparādha and kāla/parināma.
   - The three broad causes of disorder: asātmyendriyārthasaṃyoga, prajñāparādha, pariṇāma.

5. **11.45–11.49 — Three disease types and three disease paths**
   - Nija, āgantuka and mānasa disease.
   - Mental-health conduct and assessment of hita/ahita.
   - Three rogamārga: śākhā, marma/asthi/sandhi, and koṣṭha.
   - Examples of disorders associated with the three paths.

6. **11.50–11.55 — Three physician types and three medicines**
   - Bhishak classifications.
   - Distinction between physician impostors/nominal physicians and qualified practitioners.
   - Three therapeutic approaches: daivavyapāśraya, yuktivyapāśraya and sattvāvajaya.
   - For bodily doṣa disturbance: internal cleansing, external treatment, and surgical intervention.

7. **11.56–11.63 — Early intervention**
   - Wise response to disease through external/internal measures or surgery.
   - Disease may begin small and increase.
   - Delayed attention can lead to loss of strength and life.
   - The text advocates responding before disease becomes advanced.

8. **11.64–11.65 — Summary**
   - Three eṣaṇās, three upastambhas, bala, causes of disease, disease paths, physicians and medicines.
   - The closing verses summarize the chapter's recurring “threefold” architecture.

## Content-generation rules

- Preserve the exact Sanskrit source sequence and source passage labels.
- Preserve prose versus verse-half/editorial transition structure.
- Every passage must receive:
  - Sanskrit original
  - Hindi translation
  - passage-specific Hindi explanation
  - passage-specific टीका
- Do not use generic “यह श्लोक...” filler.
- Philosophical claims about आत्मा, पुनर्भव, कर्म and परलोक must be clearly framed as **classical Caraka doctrine/argument**, not as independently verified modern science.
- The discussion of mental disease and conduct should likewise remain textual/classical and should not be presented as a modern psychiatric diagnosis or treatment protocol.
- Classical physician and medicine classifications should be explained historically and academically.
- Assessment references may point only to canonical Chapter 11 passage IDs.
- Chapter 13 onward remains reserved for **AyUG-SA2 / Second Professional**.

## Integration gate

Research manifest → complete 103-passage source reconciliation → canonical Sanskrit/Hindi/व्याख्या/टीका → 20-question assessment → regression → API seeding → reader action → integration regression → tracker update.

Runtime/browser verification is separate and must not be marked passed without execution.
