# AaptaKosha Project Tracker

Last updated: 2026-10-01

| Phase | Workstream | Status | Evidence |
|---|---|---|---|
| Phase 0 | Foundation & control plane | Complete | docs/governance/phase-0-exit-criteria.md |
| Phase 1 | NCISM ingestion & reconciliation core | Complete | docs/governance/phase-1-exit-criteria.md |
| Phase 2 | Application/product layer | Complete | docs/architecture/phase-2-product-layer.md |
| Phase 3 | Knowledge & content layer | Complete | docs/architecture/phase-3-knowledge-content.md |
| Phase 4 | Assessment & learner experience | Complete | docs/architecture/phase-4-assessment-learner-experience.md |
| Phase 5 | UI/UX presentation layer | Complete | docs/architecture/phase-5-ui.md |
| Phase 6 | Durable application API & persistence | Complete | docs/architecture/phase-6-durable-api-persistence.md |
| Phase 7 | Production identity, security & operations | In progress | docs/architecture/phase-7-production-identity-security-operations.md |

## Phase 5 checklist
- [x] Responsive presentation-layer architecture
- [x] Shared design tokens and reusable visual patterns
- [x] Dashboard and learner-facing screen set
- [x] Assessment, study, practice, progress, planner, notes, notifications, and settings screens
- [x] Framework-neutral presentation layer
- [x] Representative data kept separate from domain/persistence contracts

## Phase 6 checklist
- [x] PostgreSQL assessment and learner-attempt repository
- [x] PostgreSQL learning-progress repository
- [x] Live learner-progress HTTP adapter
- [x] Vercel API wiring with PostgreSQL/SQLite backend selection
- [x] Health endpoint and operational database check
- [x] Focused Phase 6 tests
- [x] Product CI verification

### Latest Phase 6 work
- Wired durable PostgreSQL storage into the deployed API while preserving SQLite fallback.
- Added live GET/POST/PUT learner-progress routes.
- Added operational health reporting for database connectivity and backend selection.
- Added focused tests covering HTTP adapters, learner API behavior, repositories, and the real HTTP server.
- GitHub Actions product workflow run #106 completed successfully on the main branch.

## Phase 7 initial checklist
- [x] Production identity adapter
- [x] Authenticated principal propagation
- [x] Learner-resource authorization enforcement
- [ ] Production CORS and secure error handling
- [ ] Configuration/readiness validation
- [ ] Security-focused tests and CI
- [ ] Deployment verification

### Latest Phase 7 work
- Added a replaceable Clerk identity adapter using verified session tokens and explicit authorized-party validation.
- Wired authenticated principals into assessment attempts and learning-progress ownership checks at the Vercel HTTP boundary.
- Removed wildcard CORS behavior; production can allow one explicit frontend origin through `AAPTOKOSHA_ALLOWED_ORIGIN`.
- Vercel deployments fail closed when identity is required but no Clerk credentials are configured.
- Added focused Clerk adapter tests and kept Phase 7 tests in the product CI matrix.
- Deployment verification is still pending; production requires `CLERK_SECRET_KEY` or `CLERK_JWT_KEY`, `CLERK_AUTHORIZED_PARTIES`, and (for browser CORS) `AAPTOKOSHA_ALLOWED_ORIGIN`.

## Earlier completed phases

### Phase 4
- Assessment contracts, persistence, lifecycle, scoring, learner attempt API, analytics/progress integration, and CI verification are complete.

### Phase 3
- Content resources, publication lifecycle, curriculum-content linking, content API, deterministic search/index boundary, and CI expansion are complete.

### Phase 2
- Product contracts, catalog read model, application services, persistence boundary, API boundary, identity/authorization boundary, learning progress, notifications, and product CI are complete.

Tracker rule: update this file whenever a phase gate changes state.
