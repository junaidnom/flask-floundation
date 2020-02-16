from flask import make_response, redirect, render_template, request
from flask_jwt_extended import jwt_refresh_token_required
from flask_restplus import Resource, fields

from app.api.api import api
from app.api.authentication.services import authentication_service
from app.common.http import generic_response, request_response_codes
from app.data.models.identity import TenantUser
from app.api.identity.schemas import TenantUserSchema
from app.extensions import login

login_model = api.model("Login", {"username": fields.String, "password": fields.String})
refresh_model = api.model("Refresh", {"refresh_token": fields.String})

tenant_user_schema = TenantUserSchema()

@api.expect(login_model, validate=True)
class Login(Resource):
    @api.doc(responses=request_response_codes())
    def post(self):
        data = request.json
        result = authentication_service.login(data)
        return generic_response(data=result)


# NOTE The jwt_refresh_token_required decorator ensures a valid refresh
# token is present in the request before calling this endpoint.
@api.expect(refresh_model, validate=True)
class Refresh(Resource):
    @api.doc(responses=request_response_codes())
    @jwt_refresh_token_required
    def post(self):
        data = request.json
        result = authentication_service.refresh(data["refresh_token"])
        return generic_response(data=result)
