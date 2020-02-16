from flask import jsonify, url_for, request
from flask_restplus import Api, Resource, reqparse, fields
from app.common.http import request_response_codes, generic_response
from app.api.api import api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.identity.schemas import TenantSchema
from app.api.identity.services import tenant_service
from app.common.authorize import Authorize
from app.data.models.authorization import PermissionType

# Models
tenant_model = api.model("Tenant", {"id": fields.Integer, "name": fields.String})

# Schemas
tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)


@api.doc(responses=request_response_codes())
class Tenant(Resource):
    @api.doc(security="apikey")
    @jwt_required
    @Authorize([PermissionType.CAN_READ_ALL_TENANTS])
    def get(self):
        """ Gets List of all Tenants """
        result = tenants_schema.dump(tenant_service.get_all_tenants())
        return generic_response(data=result)

    @api.doc(security="apikey")
    @api.expect(tenant_model)
    @jwt_required
    @Authorize([PermissionType.CAN_CREATE_TENANT])
    def post(self):
        """Creates a Tenant
        """
        data = request.json
        tenant = tenant_schema.load(data)
        tenant_id = tenant_service.create_tenant(tenant)
        return generic_response(data=tenant_id)


@api.doc(responses=request_response_codes())
class TenantById(Resource):
    @api.doc(security="apikey")
    @jwt_required
    @Authorize([[PermissionType.CAN_READ_ALL_TENANTS, PermissionType.CAN_READ_TENANT]])
    def get(self, tenant_id):
        """ Gets a Tenant by Id
        """
        tenant = tenant_service.get_tenant_by_id(tenant_id)
        return generic_response(data=tenant_schema.dump(tenant))

    @api.doc(security="apikey")
    @api.expect(tenant_model, validate=True)
    @jwt_required
    @Authorize([PermissionType.CAN_CREATE_TENANT])
    def put(self, tenant_id):
        """ Given Tenant id update Tenant """
        data = request.json
        tenant = tenant_schema.load(data, transient=True, partial=True)
        result = tenant_schema.dump(tenant_service.update_tenant(tenant_id, tenant))
        return generic_response(data=result)
