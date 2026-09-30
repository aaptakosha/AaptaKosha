# AaptaKosha Project Tracker

Last updated: 2026-09-30

| Phase | Workstream | Status | Evidence |
|---|---|---|---|
| Phase 0 | Foundation & control plane | Complete | docs/governance/phase-0-exit-criteria.md |
| Phase 1 | NCISM ingestion & reconciliation core | Complete | docs/governance/phase-1-exit-criteria.md |
| Phase 2 | Application/product layer | Complete | docs/architecture/phase-2-product-layer.md |
| Phase 3 | Knowledge & content layer | Implementation complete; verification pending | docs/architecture/phase-3-knowledge-content.md |

## Phase 2 checklist
- [x] Product-domain contracts and catalog read model
- [x] Application use-case services
- [x] Persistence adapter and migration baseline
- [x] API boundary
- [x] Identity and authorization boundary
- [x] Learning-progress model
- [x] Notifications/automation boundary
- [x] Product-facing test and CI expansion

### Latest completed work
- Identity boundary: Principal, explicit permissions, default catalog role mappings, and AuthorizationService.
- Learning-progress boundary: domain-neutral progress snapshot, repository protocol, and application service.
- Notifications/automation boundary: provider-neutral notification queue, automation rules, channel senders, and dispatcher.
- Product-facing test and CI expansion: dedicated Phase 2 test workflow across Python 3.11 and 3.12.
- Authorization tests cover direct grants, role grants, denied permissions, missing principals, and duplicate grants.
- Production authentication remains intentionally out of scope for this phase.

## Phase 3 checklist
- [x] Content-resource contracts
- [x] Content repository and persistence boundary
- [x] Content application service and publication rules
- [x] Curriculum-to-content linking
- [x] Content API boundary
- [x] Search/indexing boundary
- [x] Phase 3 tests and CI expansion (verification pending)

### Latest Phase 3 work
- Added a deterministic, replaceable content search/index boundary with published-only indexing.
- Content application service and governed lifecycle: draft → review → published → archived, with provenance and curriculum-reference gates for publication.
- Curriculum-to-content linking is separate and auditable; links require an existing content resource and duplicate links are idempotent.
- Content API and deterministic published-only search/index boundary are implemented.
- Expanded CI to run Phase 2 and Phase 3 tests on Python 3.11 and 3.12; GitHub run verification is still pending.
- Phase 3 is **not yet marked fully verified** because an observed GitHub Actions run has not been confirmed.

Tracker rule: update this file whenever a phase gate changes state.
