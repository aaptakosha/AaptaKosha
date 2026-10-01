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

## Phase 7 checklist
- [x] Production identity adapter
- [x] Authenticated principal propagation
- [x] Learner-resource authorization enforcement
- [x] Production CORS and secure error handling
- [x] Configuration/readiness validation
- [ ] Security-focused tests and CI
- [x] Deployment verification

### Latest Phase 7 work
- Added replaceable Clerk identity adapter with verified session tokens and authorized-party validation.
- Wired authenticated principals into assessment and learning-progress ownership checks.
- Removed wildcard CORS; production can allow one explicit frontend origin through `AAPTOKOSHA_ALLOWED_ORIGIN`.
- Added structured JSON errors, CORS rejection, health/readiness reporting, and fail-closed production identity configuration.
- Fixed progress-route parsing before ownership checks and added malformed-payload/security-path coverage.
- Updated product CI so `api/**` changes trigger the Phase 2–7 test workflow.
- Verified production deployment `dpl_Aybz47q3TB2GkEY1u9BdgjhMTYjw` is READY for commit `f157d0cf7da6acbd42a64b6ff6cf1a68b13a2bc8`; GitHub's Vercel status is successful.
- The direct main-branch GitHub Actions run is not exposed by the current connector, so the security-focused CI gate remains open until an actual successful Actions run is observable.
- Production requires `CLERK_SECRET_KEY` or `CLERK_JWT_KEY`, `CLERK_AUTHORIZED_PARTIES`, and (for browser CORS) `AAPTOKOSHA_ALLOWED_ORIGIN`.

Tracker rule: update this file whenever a phase gate changes state.
