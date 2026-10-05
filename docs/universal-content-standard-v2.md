# AaptaKosha Universal Learning Content Standard v2.0

Every publishable academic chapter must satisfy the same data contract.

## Required components
- Learning objectives
- Core notes / definitions / explanation
- Tables where useful; Markdown tables are accepted
- MCQs with answers/explanations
- Exam Zone (LAQ/SAQ/viva as applicable)
- Quick Revision
- Flashcards / active-recall cards
- References / further reading

## Conditional components
- Classical Sanskrit source text, padaccheda, word meaning, translation and tika for Samhita content
- Concept maps, mind maps and diagrams whenever the topic benefits from a visual representation
- Clinical correlation where clinically applicable

## Enforcement
1. src/aaptakosha_core/content_contract.py is the canonical validator.
2. Content APIs validate before returning publishable content.
3. Invalid new/updated content must fail validation rather than silently render a partial lesson.
4. CI runs the contract tests.
5. Existing content is append-only; adding a chapter must never delete or replace unrelated chapters.
6. A content schema version is returned with validated Padartha payloads so the frontend can identify the contract in use.

## Padartha status
All 16 current Padartha Vijnanam chapters are now contract-compliant and mapped to the NCISM curriculum nodes.
