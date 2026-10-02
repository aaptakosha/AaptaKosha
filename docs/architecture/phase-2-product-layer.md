# Phase 2 — Application & Product Layer

**Status:** Phase 2 implementation complete
**Date:** 2026-09-30

## Delivered
- Immutable Curriculum, Subject, and Topic domain contracts.
- CatalogService for curriculum, subject-list, and subject retrieval.
- CatalogRepository protocol as the persistence boundary.
- Explicit CatalogNotFoundError for missing resources.
- SQLite persistence adapter and migration baseline.
- Transport-neutral catalog API boundary.
- Framework-neutral Principal and AuthorizationService contracts.
- Explicit catalog permissions and role-to-permission mapping.
- Authorization tests for direct grants, role grants, denied permissions, and missing principals.

Phase 1 remains the authoritative ingestion/reconciliation path for published curriculum. Product services consume published data and do not mutate it directly.

## Identity and authorization boundary

Authentication answers **who the caller is** and remains an adapter/provider concern. This phase defines only the stable authorization contract for an already-authenticated caller.

Principal carries:
- stable subject_id
- zero or more roles
- zero or more direct permissions

AuthorizationService evaluates a required permission from direct grants and configured role mappings. The initial catalog permissions are:
- catalog:read
- catalog:admin

The default roles are:
- catalog-reader → catalog:read
- catalog-admin → catalog:read, catalog:admin

A missing principal or missing permission is denied. No password storage, OAuth/OIDC provider, JWT library, session mechanism, or web framework is introduced at this boundary.

Transport adapters can authenticate a request, construct a Principal, and call AuthorizationService.require(...) before protected application use cases. Existing catalog API handlers remain transport-neutral and are not forced to depend on an authentication provider.

## Notifications and automation boundary

Notifications are represented by a provider-neutral `Notification` contract and queued through `NotificationRepository`. `NotificationSender` adapters isolate delivery providers such as in-app, email, push, or future channels. `AutomationRule` maps an event type and context to a notification, while `NotificationDispatcher` delivers pending records through the configured channel adapter and marks successful sends.

Scheduling, retries, provider credentials, rate limits, and external messaging APIs remain adapter/operations concerns. Unknown channels are left pending rather than marked sent. This keeps automation extensible and auditable without coupling the core to a vendor.

## Implementation sequence
1. Product-domain contracts and catalog read model — Complete
2. Application use-case services — Complete
3. Persistence adapter and migration baseline — Complete
4. API boundary — Complete
5. Identity and authorization boundary — Complete
6. Learning-progress model — Complete
7. Notifications/automation boundary — Complete
8. Product-facing test and CI expansion — Next

## Non-goals
- No production authentication.
- No password storage.
- No OAuth/OIDC/JWT/session implementation.
- No frontend.
- No vendor-specific database schema.
- No direct mutation of published curriculum from product code.
- No assumption that BAMS is the only future domain.
