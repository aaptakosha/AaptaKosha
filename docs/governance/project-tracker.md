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

## Charaka Sūtrasthāna SA-1 content pipeline
- [x] Chapter 7 research manifest and classical source verification
- [x] Chapter 7 canonical Sanskrit sequence with Hindi translation/टीका layer
- [x] Chapter 7 20-question revision assessment with canonical content references
- [x] Chapter 7 content/assessment regression contract
- [ ] Chapter 7 reader/API wiring and end-to-end learner regression
- [ ] Chapter 8+ SA-1 chapters
- [ ] Chapter 13+ remains reserved for SA-2 / Second Professional

Tracker rule: update this file whenever a phase gate changes state.
