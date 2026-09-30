# AaptaKosha Project Tracker

Last updated: 2026-09-30

| Phase | Workstream | Status | Evidence |
|---|---|---|---|
| Phase 0 | Foundation & control plane | Complete | docs/governance/phase-0-exit-criteria.md |
| Phase 1 | NCISM ingestion & reconciliation core | Complete | docs/governance/phase-1-exit-criteria.md |
| Phase 2 | Application/product layer | In progress | docs/architecture/phase-2-product-layer.md |

## Phase 2 checklist
- [x] Product-domain contracts and catalog read model
- [x] Application use-case services
- [x] Persistence adapter and migration baseline
- [x] API boundary
- [x] Identity and authorization boundary
- [x] Learning-progress model
- [ ] Notifications/automation boundary
- [ ] Product-facing test and CI expansion

### Latest completed work
- Identity boundary: Principal, explicit permissions, default catalog role mappings, and AuthorizationService.
- Learning-progress boundary: domain-neutral progress snapshot, repository protocol, and application service.
- Authorization tests cover direct grants, role grants, denied permissions, missing principals, and duplicate grants.
- Production authentication remains intentionally out of scope for this phase.

Tracker rule: update this file whenever a phase gate changes state.
