# AaptaKosha Project Tracker

Last updated: 2026-10-02

| Phase | Workstream | Status | Evidence |
|---|---|---|---|
| Phase 0 | Foundation & control plane | Complete | docs/governance/phase-0-exit-criteria.md |
| Phase 1 | NCISM ingestion & reconciliation core | Complete | docs/governance/phase-1-exit-criteria.md |
| Phase 2 | Application/product layer | Complete | docs/architecture/phase-2-product-layer.md |
| Phase 3 | Knowledge & content layer | Complete | docs/architecture/phase-3-knowledge-content.md |
| Phase 4 | Assessment & learner experience | Complete | docs/architecture/phase-4-assessment-learner-experience.md |
| Phase 5 | UI/UX presentation layer | Complete | docs/architecture/phase-5-ui.md |
| Phase 6 | Durable application API & persistence | Complete | docs/architecture/phase-6-durable-api-persistence.md |
| Phase 7 | Production identity, security & operations | Complete | docs/architecture/phase-7-production-identity-security-operations.md |
| Phase 8 | Authenticated learner experience integration | In progress | docs/architecture/phase-8-authenticated-learner-experience.md |

## Phase 8 checklist
- [x] Frontend session/bootstrap contract and shared API client
- [x] Authenticated progress integration
- [x] Assessment/practice journey integration
- [x] Shared loading/error/empty states and navigation consistency
- [ ] Integration tests and browser verification
- [ ] Production readiness verification — blocked until a production identity provider is configured

### Latest Phase 8 work
- Added provider-neutral frontend session bootstrap.
- Added reusable shared API client with optional bearer-token integration through the frontend auth provider hook.
- Wired dashboard, progress, and assessment flows through the shared boundary.
- Kept local/demo fallback behavior when no production API base is configured.
- Kept authorization decisions at the API boundary rather than in UI code.
- Added shared UI state helpers for loading, error, and empty-state messaging.
- Normalized learner navigation to real page routes across dashboard, learning, practice, assessment, progress, and notes surfaces.
- Added Phase 8 frontend contract tests and expanded CI path coverage to run them.
- Verified the latest production deployment is READY and the deployed dashboard, learn, practice, assessment, and progress routes return HTTP 200 through authenticated deployment access.
- Production /api/health currently returns HTTP 503 with identity_provider=unconfigured, identity_required=true, and ready=false; production learner API verification therefore remains blocked until Clerk production credentials/configuration are added.
- Browser verification remains open because authenticated browser interaction is not available in the current execution environment.

### Phase 7 completion evidence
- Production identity adapter, authenticated principal propagation, learner-resource authorization, CORS/error handling, configuration/readiness validation, security-focused tests, and deployment verification are complete.
- GitHub Actions product workflow run #122 completed successfully on Python 3.11 and 3.12 through PR #28.

## Deployment/integration repair — 2026-10-02

- [x] Reconciled GitHub main content with the deployed application contract
- [x] Added Vercel catalog function deployment and catalog-specific routing
- [x] Repaired broken frontend JavaScript syntax
- [x] Added Charaka Sūtrasthāna chapters 1–12 to the Samhita reader navigation
- [x] Unified reader support for both `verses` and mixed `passages` canonical content
- [x] Unified Chapter 1–12 assessment selection and results-to-content links
- [x] Production redeployment of repository repair
- [x] Live catalog/content runtime audit
- [ ] Production Clerk `CLERK_AUTHORIZED_PARTIES` configuration
- [ ] Authenticated assessment/progress runtime regression
- [ ] Live browser regression

## Charaka Sūtrasthāna 12 — Vātakalākalīya

- [x] Primary-source research and 22-record sequence reconciliation
- [x] Canonical Sanskrit sequence: 22 passages / 16 prose / 6 verse-half
- [x] Hindi translation + passage-specific व्याख्या + टीका layer
- [x] 20-question revision assessment with canonical content refs
- [x] Chapter 12 content regression test
- [x] Assessment API seeding + chapter content allow-list
- [x] Reader revision-test wiring
- [ ] Runtime/end-to-end learner regression
- [ ] Browser verification

## Charaka Sūtrasthāna 11 — Tisraiṣaṇīya

- [x] Primary-source research and 103-record sequence reconciliation
- [x] Canonical Sanskrit sequence: 103 passages / 39 prose / 64 verse-half
- [x] Hindi translation + passage-specific व्याख्या + टीका layer
- [x] 20-question revision assessment with canonical content refs
- [x] Chapter 11 content regression test
- [x] Assessment API seeding + chapter content allow-list
- [x] Reader revision-test wiring
- [ ] Runtime/end-to-end learner regression
- [ ] Browser verification

## Charaka Sūtrasthāna SA-1 content pipeline
- [x] Chapter 7 research manifest and classical source verification
- [x] Chapter 7 canonical Sanskrit sequence with Hindi translation/टीका layer (primary-source audit + verse-specific explanation/टीका completed)
- [x] Chapter 7 20-question revision assessment with canonical content references
- [x] Chapter 7 content/assessment regression contract
- [ ] Chapter 7 reader/API wiring and end-to-end learner regression
- [x] Chapter 8 research manifest and primary-source sequence verification
- [x] Chapter 8 canonical Sanskrit/Hindi/टीका content build (40 source passages; 29 prose; 11 verse-half passages)
- [x] Chapter 8 20-question revision assessment and canonical-reference contract
- [x] Chapter 8 content/assessment regression contract
- [x] Chapter 8 reader/API wiring
- [ ] Chapter 8 end-to-end learner regression
- [x] Chapter 9 primary-source research manifest and SARIT passage-sequence verification
- [x] Chapter 9 canonical Sanskrit/Hindi/टीका content build (55 passages; 3 prose; 52 verse-half passages)
- [x] Chapter 9 20-question revision assessment and canonical-reference contract
- [x] Chapter 9 content regression contract
- [x] Chapter 9 reader/API wiring
- [ ] Chapter 9 end-to-end learner regression
- [x] Chapter 10 primary-source research manifest and sequence verification
- [x] Chapter 10 canonical Sanskrit/Hindi/टीका content build
- [x] Chapter 10 20-question assessment and canonical-reference contract
- [x] Chapter 10 content regression contract
- [x] Chapter 10 reader/API wiring
- [ ] Chapter 10 end-to-end learner regression
- [ ] Chapter 11+ remaining SA-1 chapters
- [ ] Chapter 13+ remains reserved for SA-2 / Second Professional

Tracker rule: update this file whenever a phase gate changes state.

## Śārṅgadhara Saṃhitā — Madhyama Khaṇḍa
- [x] Chapter 1 — Swarasādikalpanā: source-reconciled package
- [x] Chapter 2 — Kvāthādikalpanā: source-reconciled package; extent, closing metadata and internal range references audited through verse 176
- [x] Chapter 3 — Phāṇṭādikalpanā: source-reconciled package
- [x] Chapter 4 — Himakalpanā: source-reconciled package
- [x] Chapter 5 — Kalkakalpanā: canonical Sanskrit 1–28, Hindi learning layer, commentary mapping and assessments
- [x] Chapter 6 — Cūrṇakalpanā: verified extent 1–166, canonical anchors, Hindi learning layer, commentary mapping and assessments
- [x] Chapter 7 — Vaṭakalpanā: verified extent 1–105, canonical anchors, Hindi learning layer, commentary mapping and assessments
- [x] Chapter 8 — Avalehakalpanā: verified extent 1–48, canonical anchors, Hindi learning layer, commentary mapping and assessments
- [x] Chapter 9 — Ghṛtatailakalpanā: verified extent 1–210, canonical anchors, Hindi learning layer, commentary mapping and assessments
- [x] Chapter 10 — Āsavāriṣṭādisaṃdhānakalpanā: source-reconciled package; primary online extent 1–92, printed Dīpikā numbering 1–94 preserved as a source discrepancy
- [x] Chapter 11 — Dhātuśodhanamāraṇakalpanā: verified extent 1–104, Sanskrit anchors, Hindi learning layer, Dīpikā mapping and assessments
- [x] Chapter 12 — Rasādiśodhanamāraṇakalpanā: source-reconciled final Madhyama Khaṇḍa package; audit-corrected online extent 1–293 and printed Dīpikā witness 1–295; internal range/assessment metadata audited

## Śārṅgadhara Saṃhitā — Madhyama Khaṇḍa completion
- [x] Chapters 1–12 researched, source-reconciled and committed individually
- [x] Cross-chapter extent audit: Chapter 2 corrected from 1–174 to 1–176
- [x] Chapter-level tracker coverage complete
- [ ] Full controlled printed-source verse transcription remains a future refinement for non-anchor verses
- [x] Madhyama JSON schema/regression contract added for chapter identity, witness extents, colophons, quality gates and source-safety separation
- [x] Cross-chapter audit correction: Chapter 12 witness extent discrepancy (online 1–293 vs printed 1–295) preserved explicitly


### Śārṅgadhara Saṃhitā — Uttara Khaṇḍa
- [x] Uttara Khaṇḍa chapter registry/source sequence verified: 13 chapters.
- [x] Chapter 1 — Snehapānavidhi researched and source-reconciled; primary online witness 1–33; printed Dīpikā witness 1–35 discrepancy preserved.
- [ ] Chapters 2–13 pending research-first ingestion.
