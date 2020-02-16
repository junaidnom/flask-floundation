import pytest

from ..fixtures import test_client
from app.data.models import identity, authorization

from app.common.data import seed
from app.extensions import db


@pytest.fixture(scope="function")
def sample_identity(test_client):
    # Seed Prelim data
    seed()
    # Create Tenant
    tenant = identity.Tenant()
    tenant.name = "new-test-tenant"
    db.session.add(tenant)
    db.session.commit()
    # Create Admin TenantUser
    tenant_user = identity.TenantUser()
    tenant_user.email = "test@c1.com"
    tenant_user.username = "testfixtureuser"
    tenant_user.first_name = "test"
    tenant_user.password = "1234"
    tenant_user.last_name = "user"
    tenant_user.tenant_id = tenant.id

    roles = authorization.Role.query.all()
    for role in roles:
        tenant_user.roles.append(role)
    db.session.add(tenant_user)
    db.session.commit()
    auth_token_res = test_client.post(
        "/api/v1/authentication/login",
        json={"username": tenant_user.username, "password": "1234"},
    )
    return auth_token_res.json["data"]["access_token"], tenant, tenant_user, test_client
