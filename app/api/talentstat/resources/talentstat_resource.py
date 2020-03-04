from flask import jsonify, url_for, request
from flask_restplus import Api, Resource, reqparse, fields
from app.common.http import request_response_codes, generic_response
from app.api.api import api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.talentstat.services.talentstat_service import get_result, get_result_by_id, create_test_result
from app.api.talentstat.schemas import TestResultSchema

test_result_schema = TestResultSchema()
test_result_model = api.model("TestResult", {"name": fields.String, "result": fields.String})

class TestResult(Resource):
    def get(self):
        result = get_result()
        return generic_response(data=test_result_schema.dump(result))
    
    @api.expect(test_result_model, validate=True)
    def post(self):
        data = request.json
        tenant_user = test_result_schema.load(data) #transient=True, partial=True)
        result = create_test_result(tenant_user)
        return generic_response(data=test_result_schema.dump(result))
        

class TestResultById(Resource):
    def get(self, result_id):
        result = get_result_by_id(result_id)
        return generic_response(data=test_result_schema.dump(result))
