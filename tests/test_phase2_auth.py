import pytest

from aaptakosha_core.auth import (
    AuthorizationDeniedError,
    AuthorizationService,
    CATALOG_ADMIN,
    CATALOG_READ,
    Principal,
)


def test_permission_grant_allows_protected_operation():
    principal = Principal("user-1", permissions=(CATALOG_READ,))
    AuthorizationService().require(principal, CATALOG_READ)


def test_role_grant_allows_permission():
    principal = Principal("user-1", roles=("catalog-reader",))
    AuthorizationService().require(principal, CATALOG_READ)


def test_missing_permission_is_denied():
    principal = Principal("user-1", permissions=(CATALOG_READ,))
    with pytest.raises(AuthorizationDeniedError):
        AuthorizationService().require(principal, CATALOG_ADMIN)


def test_missing_principal_is_denied():
    with pytest.raises(AuthorizationDeniedError):
        AuthorizationService().require(None, CATALOG_READ)


def test_principal_contract_rejects_duplicate_grants():
    with pytest.raises(ValueError):
        Principal("user-1", permissions=(CATALOG_READ, CATALOG_READ))
