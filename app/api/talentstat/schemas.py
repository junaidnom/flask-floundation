from app.schemas import BaseSchema
from app.data.models.talentstat import TestResult

class TestResultSchema(BaseSchema):
    class Meta:
        # fields = (
        #     "name",
        #     "result",
        # )
        model = TestResult
