from app.api.api import api
from app.api.talentstat.resources.talentstat_resource import TestResult, TestResultById

ns = api.namespace("talentstat", description="Talentstat endpoinds")
ns.add_resource(TestResult, "/test-result")
ns.add_resource(TestResultById, "/results/<int:result_id>")