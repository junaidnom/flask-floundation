from app.data.models.talentstat import TestResult
from app.extensions import db

def get_result():
    # todo actual query here
    t = TestResult()
    t.name = 'fic'
    t.result = {'lol': 5}
    return t

def get_result_by_id(_id):
    # todo actual query here
    t = TestResult.query.filter_by(id=_id).first()
    return t

def create_test_result(test_result):
    db.session.add(test_result)
    db.session.commit()
    return test_result