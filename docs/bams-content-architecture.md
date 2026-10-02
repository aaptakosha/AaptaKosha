# AaptaKosha BAMS Content Architecture

## Scope

This workstream establishes the academic navigation/layout for the first three BAMS professional years and a separate classical-text library. Detailed teaching content is intentionally deferred.

NCISM is the authoritative curriculum source for the syllabus layer. Curriculum metadata is stored separately from learning content so future syllabus revisions do not require a content rewrite.

## Academic hierarchy

Professional Year -> Subject -> Paper / Unit -> Chapter / Topic -> Learning Content

Learning content can later attach to:
- Notes
- Detailed explanations
- Short revision notes
- MCQs
- Flashcards
- PYQs
- Images / diagrams
- Videos
- References
- Clinical correlations
- Assessments

## First Professional

- AyUG-SN-AI — Sanskrit evam Ayurved Itihas
- AyUG-PV — Padartha Vijnanam
- AyUG-SA1 — Samhita Adhyayan-1
- AyUG-RS — Rachana Sharira
- AyUG-KS — Kriya Sharira

## Second Professional

- AyUG-RB — Rasashastra evam Bhaishajyakalpana
- AyUG-AT — Agada Tantra evam Vidhi Vaidyaka
- AyUG-SA2 — Samhita Adhyayan-2
- AyUG-DG — Dravyaguna Vijnana
- AyUG-RN — Roga Nidan evam Vikriti Vijnana
- AyUG-SW — Swasthavritta evam Yoga

## Third Professional

- AyUG-KC — Kayachikitsa, including Manasa Roga, Rasayana and Vajikarana
- AyUG-PK — Panchakarma & Upakarma
- AyUG-ST — Shalya Tantra
- AyUG-SL — Shalakya Tantra
- AyUG-PS — Prasuti Tantra evam Stree Roga
- AyUG-KB — Kaumarabhritya
- AyUG-SA3 — Samhita Adhyayan-3
- AyUG-EM — Atyaikachikitsa / Emergency Medicine
- AyUG-RM — Research Methodology and Medical Statistics
- Electives — stored as a separate extensible group

## Separate Samhita Library

The Samhita Library is not nested under one professional year. It is a cross-curricular classical-text catalogue.

Primary discovery groups:
1. 1st Professional
2. 2nd Professional
3. 3rd Professional
4. AIAPGET / competitive preparation
5. Brihattrayi
6. Laghutrayi
7. Other major classical texts
8. Other/lesser-known Samhita texts
9. Later compendia
10. Nighantus and reference texts

A single text may belong to multiple discovery groups without being duplicated.

## Cross-linking rule

A classical text is stored once and linked to professional-year relevance, subject relevance, syllabus topics, AIAPGET tags, chapter/adhyaya where applicable, and commentary/edition metadata.

## Content status

Each curriculum node and classical text supports: planned, structure_ready, content_in_progress, review, published.

At this stage the three-professional structure is structure_ready; detailed content remains planned.

## NCISM hierarchy ingestion status

The database now supports the full hierarchy:
**Professional Year -> Subject -> Paper -> Unit/Chapter -> Topic**.

A first source-verified structural batch has been added for:
- 1st Professional: AyUG-PV, AyUG-RS, AyUG-KS, AyUG-SA1 (verified structural chapter layout)
- 2nd Professional: AyUG-RB, AyUG-AT, AyUG-SA2, AyUG-DG, AyUG-SW (AyUG-SA2 now includes all 54 prescribed chapters)

The nodes store the NCISM source reference, source locator, term, marks, lecture hours and non-lecture hours where the source table provides them.

Third Professional subject shells remain in place and are ready for the same source-verified ingestion pass. No third-professional topic data is being guessed or copied from non-NCISM summaries.

### Source verification examples

- NCISM first-professional AyUG-PV curriculum: Table 2 lists the course topics and term/hour structure.
- NCISM first-professional AyUG-RS curriculum: Table 2 lists Paper I topics such as Shariropkramaniya Shaarira, Paribhasha Shaarira and Garbha Shaarira.
- NCISM first-professional AyUG-KS curriculum: Table 2 lists topics such as Sharir, Basic principles of Ayurveda and Tridosha.
- NCISM second-professional AyUG-RB, AyUG-AT, AyUG-SA2, AyUG-DG and AyUG-SW curriculum documents provide the corresponding paper/topic structures.

This is a structural ingestion layer only. Detailed learning content, explanations, MCQs, flashcards and other study assets remain a separate later phase.
