from app.data.models import identity, authorization
from app.data.models.authorization import PermissionType
from flask_jwt_extended import get_jwt_claims
from app.extensions import db
from flask import abort


def check_tenant_authorization(tenant_id, override_permission=None):
    """ Checks if claims user belongs to Tenant or has override permissions
        to edit other Tenants
    """
    claims = get_jwt_claims()
    if "id" in list(claims.keys()):
        tenant_user = identity.TenantUser.query.filter_by(id=claims["id"]).first()
        if (
            tenant_user.tenant_id == tenant_id
            or override_permission in tenant_user.permissions
        ):
            return
    abort(403, "Unauthorized Tenant")


def create_tenant(tenant):
    """Given a tenant schema, create a tenant"""
    exists = identity.Tenant.query.filter_by(name=tenant.name).first()
    if exists:
        abort(409, "Tenant Already Exists")
    db.session.add(tenant)
    db.session.commit()
    return tenant.id


def update_tenant(tenant_id, new_tenant):
    """ Given tenant_id and tenant object, update a Tenant"""
    check_tenant_authorization(tenant_id)
    new_tenant.id = tenant_id
    updated_tenant = db.session.merge(new_tenant)
    db.session.commit()
    return updated_tenant


def get_tenant_by_id(tenant_id):
    """Given a tenant id, fetch the tenant for that id"""
    tenant = identity.Tenant.query.filter_by(id=tenant_id).first()
    if tenant:
        return tenant
    abort(404, f"Unable to find tenant with id: {tenant_id}")


def get_all_tenants():
    """ Provides list of all Tenants"""
    tenants = identity.Tenant.query.all()
    return tenants
