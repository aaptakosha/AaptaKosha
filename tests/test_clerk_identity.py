import pytest

from aaptakosha_core.clerk_identity import (
    ClerkConfigurationError,
    ClerkIdentityProvider,
    build_identity_provider,
)


def test_clerk_is_disabled_when_no_credentials_are_configured(monkeypatch):
    monkeypatch.delenv("CLERK_SECRET_KEY", raising=False)
    monkeypatch.delenv("CLERK_JWT_KEY", raising=False)
    monkeypatch.delenv("CLERK_AUTHORIZED_PARTIES", raising=False)

    assert build_identity_provider() is None


def test_partial_clerk_configuration_fails_with_actionable_error(monkeypatch):
    monkeypatch.setenv("CLERK_SECRET_KEY", "test-secret")
    monkeypatch.delenv("CLERK_JWT_KEY", raising=False)
    monkeypatch.delenv("CLERK_AUTHORIZED_PARTIES", raising=False)

    with pytest.raises(ClerkConfigurationError, match="CLERK_AUTHORIZED_PARTIES"):
        build_identity_provider()


def test_clerk_authorized_parties_are_trimmed_and_split(monkeypatch):
    monkeypatch.setenv("CLERK_SECRET_KEY", "test-secret")
    monkeypatch.setenv(
        "CLERK_AUTHORIZED_PARTIES",
        " https://aapta-kosha.vercel.app, https://www.aaptakosha.example ",
    )

    provider = build_identity_provider()

    assert isinstance(provider, ClerkIdentityProvider)
    assert provider._authorized_parties == (
        "https://aapta-kosha.vercel.app",
        "https://www.aaptakosha.example",
    )
