from ..fixtures import test_client
from app.extensions import app, db
from uuid import uuid4
from app.data.models import identity
from app.api.identity.services import tenant_service, tenant_user_service
from app.api.identity.schemas import (
    TenantSchema,
    TenantUserSchema,
    TenantUserCreationSchema,
)


def test_tenant(test_client):
    """Test tenant creation and fetching"""
    tenant_schema = TenantSchema()
    t1 = tenant_schema.load({"name": "Correlation One"})
    none_search = identity.Tenant.query.filter_by(name="Correlation One").first()

    assert none_search is None

    tenant_service.create_tenant(t1)
    some_search = identity.Tenant.query.filter_by(name="Correlation One").first()

    assert some_search is not None


def test_tenant_user(test_client):
    tenant_schema = TenantSchema()
    t1 = tenant_schema.load({"name": "TestCo"})
    tenant_service.create_tenant(t1)
    tenant_obj = identity.Tenant.query.filter_by(name=t1.name).first()

    tenant_user_schema = TenantUserCreationSchema()
    tu1 = tenant_user_schema.load(
        {
            "username": "bobby_b",
            "first_name": "Bobby",
            "last_name": "[B]aratheon",
            "password": "bo@rB0rer",
            "email": "king@westeros.net",
            "tenant_id": tenant_obj.id,
        }
    )

    none_search = identity.TenantUser.query.filter_by(username=tu1.username).first()

    assert none_search is None

    tenant_user_service.create_tenant_user(tu1)
    some_search = identity.TenantUser.query.filter_by(username=tu1.username).first()

    assert some_search is not None
