from app.data.models import identity
from app.data.models.authorization import PermissionType
from app.extensions import db
from flask import abort
from flask_jwt_extended import get_jwt_claims
from app.common.authorize import get_claims_user


def create_tenant_user(tenant_user):
    """Given a tenant user schema, create a tenant user"""
    exists = identity.TenantUser.query.filter_by(username=tenant_user.username).first()
    if exists:
        abort(409, "TenantUser already exists")
    db.session.add(tenant_user)
    db.session.commit()
    return tenant_user


def update_tenant_user(tenant_user_id, new_tenant_user):
    """ Given a TenantUser id and a tenant_user_object, update a tenant_user
    """
    new_tenant_user.id = tenant_user_id
    claims_user = get_claims_user()
    if new_tenant_user in db.session:
        db.session.expunge(new_tenant_user)
    # Check that claims user belongs to the tenant being created or has
    # override permission
    old_tenant_user = identity.TenantUser.query.filter_by(id=tenant_user_id).first()
    # Check that user actually exists
    if not old_tenant_user:
        abort(404, "Tenant User does not exist")
    # Check if claims user belongs to tenant they are attempting to update
    # Then check if the claims user is moving the TenantUser to a new Tenant
    # If so check for override permissions
    if (
        claims_user.tenant_id != old_tenant_user.tenant_id
        or old_tenant_user.tenant_id != new_tenant_user.tenant_id
    ) and not claims_user.has_permission(PermissionType.CAN_CREATE_ALL_TENANT_USERS):
        abort(403, "Unauthorized : Invalid Permissions")

    updated_tenant_user = db.session.merge(new_tenant_user)
    db.session.commit()
    return updated_tenant_user


def get_tenant_user_by_id(tenant_user_id):
    """Given a tenant user id, fetch the tenant user for that id"""
    tenant_user = identity.TenantUser.query.filter_by(id=tenant_user_id).first()
    if tenant_user:
        return tenant_user
        abort(409, f"Tennat User does not exist : {tenant_user_id}")


def get_tenant_users_by_tenant_id(tenant_id):
    claims_user = get_claims_user()
    if claims_user.tenant_id != tenant_id and not claims_user.has_permission(
        PermissionType.CAN_READ_ALL_TENANT_USERS
    ):
        abort(403, "Unauthorized")
    tenant_users = identity.TenantUser.query.filter_by(tenant_id=tenant_id).all()
    return tenant_users
