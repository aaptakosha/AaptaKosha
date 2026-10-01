import sys
import types

import pytest

from aaptakosha_core.clerk_identity import ClerkIdentityProvider, build_identity_provider
from aaptakosha_core.auth import Principal


def test_clerk_provider_requires_explicit_authorized_parties():
    with pytest.raises(ValueError, match="CLERK_AUTHORIZED_PARTIES"):
        ClerkIdentityProvider(secret_key="secret", jwt_key=None, authorized_parties=[])


def test_clerk_provider_resolves_verified_subject(monkeypatch):
    captured = {}

    class FakeState:
        is_signed_in = True
        payload = {"sub": "user_123"}

    class FakeOptions:
        def __init__(self, **kwargs):
            captured["options"] = kwargs

    def fake_authenticate_request(request, options):
        captured["request"] = request
        return FakeState()

    fake_module = types.SimpleNamespace(
        AuthenticateRequestOptions=FakeOptions,
        authenticate_request=fake_authenticate_request,
    )
    monkeypatch.setitem(sys.modules, "clerk_backend_api", fake_module)

    provider = ClerkIdentityProvider(
        secret_key="secret",
        jwt_key="public-key",
        authorized_parties=["https://app.example"],
    )
    request = types.SimpleNamespace(headers={"Authorization": "Bearer token"})
    principal = provider.resolve(request)

    assert principal == Principal("user_123")
    assert captured["request"] is request
    assert captured["options"]["secret_key"] == "secret"
    assert captured["options"]["jwt_key"] == "public-key"
    assert captured["options"]["authorized_parties"] == ["https://app.example"]
    assert captured["options"]["accepts_token"] == ["session_token"]


def test_identity_provider_is_disabled_without_clerk_credentials(monkeypatch):
    monkeypatch.delenv("CLERK_SECRET_KEY", raising=False)
    monkeypatch.delenv("CLERK_JWT_KEY", raising=False)
    assert build_identity_provider() is None


def test_identity_provider_requires_configuration_when_credentials_exist(monkeypatch):
    monkeypatch.setenv("CLERK_JWT_KEY", "public-key")
    monkeypatch.delenv("CLERK_SECRET_KEY", raising=False)
    monkeypatch.delenv("CLERK_AUTHORIZED_PARTIES", raising=False)
    with pytest.raises(ValueError, match="CLERK_AUTHORIZED_PARTIES"):
        build_identity_provider()
