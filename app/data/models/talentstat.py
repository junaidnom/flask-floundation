from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app.common.utils import represent

class TestResult(db.Model):
    __tablename__ = "test_result"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    result = db.Column(db.String(20000))
    # users = db.relationship("TenantUser", backref=db.backref("tenant"), lazy="dynamic")
    # roles = db.relationship(
    #     "Role",
    #     secondary=role_to_tenant,
    #     lazy=True,
    #     backref=db.backref("tenant", lazy="dynamic"),
    # )

    # @classmethod
    # def find_by_name(self, name):
    #     return self.query.filter_by(name=name).first()

    # @hybrid_property
    # def name(self):
    #     return self.first_name + " " + self.last_name

    def __repr__(self):
        return represent(self, f"{str(self.name)}_{str(self.id)}")