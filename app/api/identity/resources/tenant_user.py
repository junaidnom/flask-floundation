from flask import jsonify, url_for, request
from flask_restplus import Api, Resource, reqparse, fields
from app.common.http import request_response_codes, generic_response
from app.api.api import api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.identity.schemas import TenantUserSchema, TenantUserCreationSchema
from app.api.identity.services import tenant_user_service
from app.common.authorize import Authorize
from app.data.models.authorization import PermissionType
from app.data.models import identity

# Models
role_model = api.model("Role", {"id": fields.Integer, "name": fields.String})
tenant_user_model = api.model(
    "TenantUser",
    {
        "id": fields.Integer,
        "tenant_id": fields.Integer,
        "email": fields.String,
        "password": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "username": fields.String,
        "roles": fields.List(fields.Nested(role_model)),
    },
)

# Schemas
tenant_user_schema = TenantUserSchema()
tenant_users_schema = TenantUserSchema(many=True)
tenant_user_creation_schema = TenantUserCreationSchema()


@api.doc(responses=request_response_codes())
class TenantUserById(Resource):
    @api.doc(security="apikey")
    @jwt_required
    @Authorize([PermissionType.CAN_READ_TENANT_USER])
    def get(self, tenant_user_id):
        """ Gets TenantUser by Id """
        tenant_user = tenant_user_service.get_tenant_user_by_id(tenant_user_id)
        return generic_response(data=tenant_user_schema.dump(tenant_user))

    @api.doc(security="apikey")
    @api.expect(tenant_user_model)
    @jwt_required
    @Authorize([PermissionType.CAN_CREATE_TENANT_USER])
    def put(self, tenant_user_id):
        """ Updates TenantUser by Id"""
        data = request.json
        tenant_user = tenant_user_schema.load(data, transient=True, partial=True)
        result = tenant_user_schema.dump(
            tenant_user_service.update_tenant_user(tenant_user_id, tenant_user)
        )
        return generic_response(data=result)


@api.doc(responses=request_response_codes())
class TenantUser(Resource):
    @api.doc(security="apikey")
    @jwt_required
    @api.expect(tenant_user_model)
    @Authorize([PermissionType.CAN_CREATE_TENANT_USER])
    def post(self):
        """Creates a tenant user"""
        data = request.json
        tenant_user = tenant_user_creation_schema.load(data)
        result = tenant_user_service.create_tenant_user(tenant_user)
        return generic_response(data=tenant_user_schema.dump(result))


@api.doc(responses=request_response_codes())
class TenantUsersByTenantId(Resource):
    @api.doc(security="apikey")
    @jwt_required
    @Authorize(
        [PermissionType.CAN_READ_ALL_TENANT_USERS, PermissionType.CAN_READ_TENANT_USER]
    )
    def get(self, tenant_id):
        """ Get list of Tenant Users given a Tenant id"""
        result = tenant_users_schema.dump(
            tenant_user_service.get_tenant_users_by_tenant_id(tenant_id)
        )
        return generic_response(data=result)
