import json

from ..fixtures import test_client
from test.identity.fixtures import sample_identity
from app.data.models import identity, authorization
from app.api.identity import schemas as id_schemas
from app.api.identity.services import tenant_service, tenant_user_service
from app.extensions import db
import uuid


def test_tenant_update(sample_identity):
    """ Tests updating aesthetic fields on Tenant """
    access_token, tenant, tenant_user, tc = sample_identity
    tenant.name = "ilovebeansllc"
    headers = {"Authorization": "Bearer " + access_token}
    updated_tenant_request = id_schemas.TenantSchema().dump(tenant)
    updated_tenant = tc.put(
        f"api/v1/identity/tenant/{tenant.id}",
        json=updated_tenant_request,
        headers=headers,
    )
    assert updated_tenant.status_code == 200, "Tenant could not be updated"


def test_tenant_user_create(sample_identity):
    access_token, tenant, tenant_user, tc = sample_identity
    headers = {"Authorization": "Bearer " + access_token}
    tenant_user_json = {
        "username": "mrhotdog",
        "password": "1234",
        "tenant_id": tenant.id,
    }
    tenant_user_request = tc.post(
        "api/v1/identity/tenant-user", json=tenant_user_json, headers=headers
    )
    assert tenant_user_request.status_code == 200, "Create Failed, received non 200"
    assert (
        tenant_user_request.json["data"]["username"] == tenant_user_json["username"]
    ), "Response Data does not match"
    assert (
        tenant_user_request.json["data"]["tenant_id"] == tenant_user_json["tenant_id"]
    ), "Response Data does not match"


def test_tenant_user_aesthetic_update(sample_identity):
    """ Tests aesthetic updates for tenant_user """
    access_token, tenant, tenant_user, tc = sample_identity
    headers = {"Authorization": "Bearer " + access_token}
    new_email = f"{uuid.uuid4()}@c1.com"
    new_first_name = str(uuid.uuid4())
    new_last_name = str(uuid.uuid4())
    updated_tenant_user = {"first_name": new_first_name, "last_name": new_last_name}
    update_request = tc.put(
        f"api/v1/identity/tenant-user/{tenant_user.id}",
        json=updated_tenant_user,
        headers=headers,
    )
    assert update_request.status_code == 200, "Update Failed with non 200 error code"
    assert update_request.json["data"]["first_name"] == new_first_name
    assert update_request.json["data"]["last_name"] == new_last_name


def test_tenant_user_change_tenant(sample_identity):
    """ Tests authorization around limiting re-assignment of
        TenantUsers by non-administrators
    """
    access_token, tenant, tenant_user, tc = sample_identity
    # Create a new Tenant
    new_tenant = identity.Tenant()
    new_tenant.name = "Aperture Science"
    db.session.add(new_tenant)
    db.session.commit()
    # Create a Tenant Specific admin role
    new_special_role = authorization.Role()
    # Assign ability to create a user on specific tenant to the new role but
    # not the ability to create user on ANY tenant
    can_create_tenant_user = authorization.Permission.query.filter_by(
        name=authorization.PermissionType.CAN_CREATE_TENANT_USER.value
    ).first()
    new_special_role.permissions.append(can_create_tenant_user)
    db.session.add(new_special_role)
    db.session.commit()
    # Create a new TenantUser assigned to new Tenant
    new_tenant_user = identity.TenantUser()
    new_tenant_user.username = "gordonfreeman"
    new_tenant_user.tenant_id = new_tenant.id
    new_tenant_user.password = "1234"
    new_tenant_user.roles.append(new_special_role)
    db.session.add(new_tenant_user)
    db.session.commit()
    # Login new user
    new_access_token = tc.post(
        "api/v1/authentication/login",
        json={"username": new_tenant_user.username, "password": "1234"},
    ).json["data"]["access_token"]

    # Try to re-assign original tenant_user to new tenant
    headers = {"Authorization": "Bearer " + new_access_token}
    tenant_user_json = id_schemas.TenantUserSchema().dump(tenant_user)
    tenant_user_json["tenant_id"] = new_tenant_user.tenant_id
    response = tc.put(
        f"api/v1/identity/tenant-user/{tenant_user.id}",
        json=tenant_user_json,
        headers=headers,
    )
    # Assert that permission is blocked
    assert response.status_code == 403, "Tenant Permission assignment not blocking"

    # Login with admin user
    new_access_token = tc.post(
        "api/v1/authentication/login",
        json={"username": tenant_user.username, "password": "1234"},
    ).json["data"]["access_token"]
    # Attempt to Change tenant of new_tenant_user
    headers = {"Authorization": "Bearer " + new_access_token}
    tenant_user_json = id_schemas.TenantUserSchema().dump(new_tenant_user)
    tenant_user_json["tenant_id"] = tenant.id
    response = tc.put(
        f"api/v1/identity/tenant-user/{new_tenant_user.id}",
        json=tenant_user_json,
        headers=headers,
    )
    assert response.status_code == 200, "Tenant change permission blocking"


def test_get_tenant_by_id(sample_identity):
    """ Gets Tenant By ID """
    access_token, tenant, tenant_user, tc = sample_identity
    new_access_token = tc.post(
        "api/v1/authentication/login",
        json={"username": tenant_user.username, "password": "1234"},
    ).json["data"]["access_token"]
    headers = {"Authorization": "Bearer " + new_access_token}
    response = tc.get(f"api/v1/identity/tenant/{tenant.id}", headers=headers)
    assert response.status_code == 200, "Failed to fetch Tenant By ID"
    assert response.json["data"]["name"] == tenant.name, "Tenant name doesn't match"


def test_get_tenant_user_by_id(sample_identity):
    """ Gets Tenant User By ID """
    access_token, tenant, tenant_user, tc = sample_identity
    new_access_token = tc.post(
        "api/v1/authentication/login",
        json={"username": tenant_user.username, "password": "1234"},
    ).json["data"]["access_token"]
    headers = {"Authorization": "Bearer " + new_access_token}
    response = tc.get(f"api/v1/identity/tenant-user/{tenant_user.id}", headers=headers)
    assert response.status_code == 200, "Failed to fetch TenantUser By ID"
    assert (
        response.json["data"]["username"] == tenant_user.username
    ), "TenantUser username doesn't match"


def test_get_all_tenants(sample_identity):
    access_token, tenant, tenant_user, tc = sample_identity
    new_access_token = tc.post(
        "api/v1/authentication/login",
        json={"username": tenant_user.username, "password": "1234"},
    ).json["data"]["access_token"]
    headers = {"Authorization": "Bearer " + new_access_token}
    response = tc.get(f"api/v1/identity/tenant", headers=headers)

    assert response.status_code == 200, "Failed to fetch Tenant list"
    assert isinstance(response.json["data"], list), "Tenant List returning invalid type"
    assert len(response.json["data"]) > 0, "Tenant list provided no data"
    for idx, t in enumerate(response.json["data"]):
        assert "name" in list(t.keys())
        assert "id" in list(t.keys())

def test_get_tenant_users_by_tenant_id(sample_identity):
    access_token, tenant, tenant_user, tc = sample_identity
    new_access_token = tc.post(
        "api/v1/authentication/login",
        json={"username": tenant_user.username, "password": "1234"},
    ).json["data"]["access_token"]
    headers = {"Authorization": "Bearer " + new_access_token}
    response = tc.get(f"api/v1/identity/tenant/{tenant.id}/tenant-users", headers=headers)
    assert response.status_code == 200, "Failed to fetch Tenant list"
    assert isinstance(response.json["data"], list), "Tenant List returning invalid type"
    assert len(response.json["data"]) > 0, "Tenant list provided no data"
    for idx, t in enumerate(response.json["data"]):
        assert "username" in list(t.keys())
        assert "id" in list(t.keys())
        assert "password" not in list(t.keys())
    return
