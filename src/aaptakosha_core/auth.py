"""Framework-neutral identity and authorization contracts for AaptaKosha.

Authentication providers are intentionally out of scope here. This module models
an already-authenticated principal and the authorization checks that application
adapters can perform before invoking protected use cases.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping, Protocol, Tuple


CATALOG_READ = "catalog:read"
CATALOG_ADMIN = "catalog:admin"


class IdentityProvider(Protocol):
    """Resolve a request into an already-authenticated principal."""

    def resolve(self, request: Any) -> Principal | None: ...


@dataclass(frozen=True)
class Principal:
    """Stable caller identity plus explicitly granted roles and permissions."""

    subject_id: str
    roles: Tuple[str, ...] = ()
    permissions: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.subject_id.strip():
            raise ValueError("subject_id must be non-empty")
        if len(set(self.roles)) != len(self.roles):
            raise ValueError("roles must be unique")
        if len(set(self.permissions)) != len(self.permissions):
            raise ValueError("permissions must be unique")


class AuthorizationDeniedError(PermissionError):
    """Raised when a principal cannot perform a protected operation."""


DEFAULT_ROLE_PERMISSIONS: Mapping[str, Tuple[str, ...]] = MappingProxyType(
    {
        "catalog-reader": (CATALOG_READ,),
        "catalog-admin": (CATALOG_READ, CATALOG_ADMIN),
    }
)


class AuthorizationService:
    """Evaluate permissions without coupling to a user/authentication provider."""

    def __init__(
        self,
        role_permissions: Mapping[str, Tuple[str, ...]] | None = None,
    ) -> None:
        self._role_permissions = MappingProxyType(
            dict(role_permissions or DEFAULT_ROLE_PERMISSIONS)
        )

    def has_permission(self, principal: Principal | None, permission: str) -> bool:
        if not permission.strip() or principal is None:
            return False
        granted = set(principal.permissions)
        for role in principal.roles:
            granted.update(self._role_permissions.get(role, ()))
        return permission in granted

    def require(self, principal: Principal | None, permission: str) -> None:
        if not self.has_permission(principal, permission):
            raise AuthorizationDeniedError(
                f"permission denied: {permission}"
            )


__all__ = [
    "IdentityProvider",
    "AuthorizationDeniedError",
    "AuthorizationService",
    "CATALOG_ADMIN",
    "CATALOG_READ",
    "DEFAULT_ROLE_PERMISSIONS",
    "Principal",
]
