# Phase 7 — Production Identity, Security & Operations

**Status:** Complete  
**Date:** 2026-10-01

## Purpose

Phase 7 hardens the deployed AaptaKosha application for real learners without coupling authentication, authorization, security controls, or operational concerns into the existing domain contracts.

## Scope

### Identity
- Introduce a production authentication boundary. The current adapter uses Clerk session-token verification while keeping the core identity contract provider-neutral.
- Resolve a stable learner identity at the HTTP boundary.
- Keep learner identity separate from curriculum and content identifiers.
- Preserve the existing authorization service as the policy boundary.

### API security
- Remove anonymous access to learner-specific reads/writes where production identity is required.
- Enforce learner ownership on assessment attempts and learning progress.
- Validate request payloads and reject malformed or unsafe input consistently.
- Define CORS policy for production rather than relying on a wildcard; `AAPTOKOSHA_ALLOWED_ORIGIN` controls the explicit allowed origin.
- Add rate-limit hooks at the transport/deployment boundary.

### Secrets and configuration
- Keep DATABASE_URL and future provider credentials out of source control.
- Define environment-specific configuration expectations. Production identity uses `CLERK_SECRET_KEY` or `CLERK_JWT_KEY` plus a non-empty `CLERK_AUTHORIZED_PARTIES` allowlist.
- Add startup/configuration validation that does not reveal secret values. Vercel deployments fail closed with a configuration error when identity is required but no provider is configured.

### Operations
- Expand health/readiness checks without exposing sensitive data.
- Add structured application error categories suitable for monitoring.
- Document deployment, rollback, and database migration expectations.
- Preserve SQLite local fallback while making production configuration explicit.

### Verification
- Added focused Phase 7 tests for identity propagation, learner isolation, authorization failures, malformed requests, CORS behavior, and configuration safety.
- Kept the existing Phase 0–6 regression suite green.
- Verified GitHub Actions product workflow run #122 successfully on Python 3.11 and 3.12.
- Verified production deployment `dpl_Aybz47q3TB2GkEY1u9BdgjhMTYjw` reached READY with a successful Vercel status.

## Architectural constraints

- NCISM curriculum remains authoritative.
- Existing assessment, content, catalog, progress, and persistence contracts remain reusable.
- Authentication providers are replaceable behind an identity adapter.
- UI code consumes authenticated API contracts and does not implement authorization rules.
- No secret, token, or credential is committed to the repository.

## Initial implementation order

1. Identity adapter contract and authenticated principal propagation.
2. Production authorization enforcement for learner-owned resources.
3. Secure HTTP/CORS/error handling.
4. Configuration and readiness validation.
5. Focused tests and CI.
6. Deployment verification.

## Non-goals

- Replacing the existing domain model.
- Building a custom password-management system when a supported identity provider can provide the capability.
- Introducing AI-generated content as part of security work.
- Adding product analytics unrelated to operational/security requirements.
