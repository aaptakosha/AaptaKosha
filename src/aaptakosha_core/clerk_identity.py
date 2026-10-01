"""Production identity adapter for the Vercel HTTP boundary.

The core domain only receives an already-authenticated Principal. Clerk-specific
verification stays in this transport adapter so the domain remains provider-neutral.
"""
from __future__ import annotations

import os
from typing import Any

from .auth import IdentityProvider, Principal


def _csv(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


class ClerkIdentityProvider:
    """Verify Clerk session tokens and convert the verified subject to Principal."""

    def __init__(
        self,
        *,
        secret_key: str | None,
        jwt_key: str | None,
        authorized_parties: list[str],
    ) -> None:
        self._secret_key = (secret_key or "").strip()
        self._jwt_key = (jwt_key or "").strip()
        self._authorized_parties = tuple(authorized_parties)
        if not self._secret_key and not self._jwt_key:
            raise ValueError("CLERK_SECRET_KEY or CLERK_JWT_KEY is required")
        if not self._authorized_parties:
            raise ValueError("CLERK_AUTHORIZED_PARTIES must not be empty")

    @classmethod
    def from_environment(cls) -> "ClerkIdentityProvider":
        return cls(
            secret_key=os.environ.get("CLERK_SECRET_KEY"),
            jwt_key=os.environ.get("CLERK_JWT_KEY"),
            authorized_parties=_csv(os.environ.get("CLERK_AUTHORIZED_PARTIES")),
        )

    def resolve(self, request: Any) -> Principal | None:
        # Imported lazily so framework-neutral tests can exercise the boundary
        # without importing the external provider until production auth is used.
        from clerk_backend_api import AuthenticateRequestOptions, authenticate_request

        state = authenticate_request(
            request,
            AuthenticateRequestOptions(
                secret_key=self._secret_key or None,
                jwt_key=self._jwt_key or None,
                authorized_parties=list(self._authorized_parties),
                accepts_token=["session_token"],
            ),
        )
        if not state.is_signed_in:
            return None

        payload = state.payload or {}
        subject = str(payload.get("sub", "")).strip()
        return Principal(subject) if subject else None


def build_identity_provider() -> IdentityProvider | None:
    """Return the configured production provider, or None when auth is disabled."""
    configured = any(
        os.environ.get(name, "").strip()
        for name in ("CLERK_SECRET_KEY", "CLERK_JWT_KEY")
    )
    if not configured:
        return None
    return ClerkIdentityProvider.from_environment()


__all__ = ["ClerkIdentityProvider", "build_identity_provider"]
