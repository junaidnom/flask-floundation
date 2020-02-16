from flask import Blueprint, jsonify, url_for
from flask_restplus import Api, Resource, reqparse
from app.api.api import api
from app.api.identity.resources.tenant_user import (
    TenantUser,
    TenantUserById,
    TenantUsersByTenantId,
)
from app.api.identity.resources.tenant import Tenant, TenantById

# NOTE: Define namespace for route scoping
ns = api.namespace("identity", description="Identity Endpoints")
ns.add_resource(TenantUser, "/tenant-user")
ns.add_resource(TenantUserById, "/tenant-user/<int:tenant_user_id>")
ns.add_resource(TenantUsersByTenantId, "/tenant/<int:tenant_id>/tenant-users")
ns.add_resource(Tenant, "/tenant")
ns.add_resource(TenantById, "/tenant/<int:tenant_id>")
