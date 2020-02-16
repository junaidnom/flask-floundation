import pytest
from app.extensions import app, db
from app.data.models import authorization, identity
from app.api.authorization import schemas as authorization_schemas
from ..fixtures import test_client
from uuid import uuid4


def test_role_create(test_client):

    role_schema = authorization_schemas.RoleSchema()
    none_search = authorization.Role.query.filter_by(name="test-admin").first()

    assert none_search is None
    new_role = authorization.Role(name="test-admin")
    db.session.add(new_role)
    db.session.commit()

    some_search = authorization.Role.query.filter_by(name="test-admin").first()
    assert some_search is not None


def test_permission_create(test_client):
    permission_schema = authorization_schemas.PermissionSchema()
    none_search = authorization.Permission.query.filter_by(
        name="test-permission"
    ).first()

    assert none_search is None

    new_permission = authorization.Permission(name="test-permission")
    db.session.add(new_permission)
    db.session.commit()

    some_search = authorization.Permission.query.filter_by(
        name="test-permission"
    ).first()
    dump_schema = permission_schema.dump(some_search)
    assert some_search is not None
    assert dump_schema is not None


def test_assign_permission_to_role(test_client):
    permission_name = uuid4()
    new_permission = authorization.Permission(name=permission_name)
    db.session.add(new_permission)
    db.session.commit()

    role_name = uuid4()
    new_role = authorization.Role(name=role_name)
    db.session.add(new_role)
    db.session.commit()

    statement = authorization.role_to_permission.insert().values(
        role_id=new_role.id, permission_id=new_permission.id
    )
    db.session.execute(statement)
    db.session.commit()

    r2p = (
        db.session.query(authorization.role_to_permission)
        .filter(
            authorization.role_to_permission.c.role_id == new_role.id,
            authorization.role_to_permission.c.permission_id == new_permission.id,
        )
        .first()
    )
    assert r2p is not None
    assert r2p.role_id == new_role.id
    assert r2p.permission_id == new_permission.id


def test_assign_default_role_to_tenant(test_client):
    """
    Tests assignment of default roles to a Tenant
    when the Tenant is created
    """
    new_role = authorization.Role(name=uuid4(), is_default=True)
    new_tenant = identity.Tenant(name=uuid4())
    db.session.add(new_role)
    db.session.commit()
    db.session.add(new_tenant)
    db.session.commit()
    default_role_ids = [
        r.id for r in authorization.Role.query.filter_by(is_default=True).all()
    ]
    tenant_role_ids = [r.id for r in new_tenant.roles]

    assert new_role.id in tenant_role_ids
