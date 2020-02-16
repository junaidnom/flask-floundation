import os
from uuid import uuid4

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm.session import object_session
from sqlalchemy.orm.attributes import set_committed_value
from app.common.utils import represent
from app.extensions import bcrypt, db, jwt
from app.schemas import BaseSchema
from flask_login import UserMixin
from app.extensions import login
from app.data.models.authorization import (
    role_to_tenant_user,
    role_to_tenant,
    Role,
)
from app.api.authorization import schemas as authorization_schemas
from marshmallow import fields
from sqlalchemy import event

# Must define model and Schema
class TenantUser(db.Model, UserMixin):
    __tablename__ = "tenant_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    _password = db.Column(db.String(250), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"), nullable=False)
    roles = db.relationship(
        "Role",
        secondary=role_to_tenant_user,
        lazy=False,
        backref=db.backref("tenant_users", lazy=True),
    )

    @hybrid_property
    def permissions(self):
        permissions = [p for r in self.roles for p in r.permissions]
        return permissions

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        if new_password != self._password:
            pw_hash = generate_password_hash(new_password)
            self._password = pw_hash

    @hybrid_method
    def has_permission(self, permission):
        return permission.value in [p.name for p in self.permissions]

    @classmethod
    def find_by_username(self, username):
        return self.query.filter_by(username=username).first()

    def __repr__(self):
        return represent(self, self.username)


"""
Define default behavior for jwt identity
and claims loaders.
"""

@jwt.user_claims_loader
def add_claims_to_token(tenant_user):
    role_schema = authorization_schemas.RoleSchema(many=True)
    return {
        "id": tenant_user.id,
        "roles": role_schema.dump(tenant_user.roles),
        "tenant_id": tenant_user.tenant_id,
    }


@jwt.user_identity_loader
def user_identity_lookup(tenant_user):
    return tenant_user.username


@login.user_loader
def load_user(tenant_user_id):
    return TenantUser.query.filter_by(id=tenant_user_id).first()


class Tenant(db.Model):
    __tablename__ = "tenant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    users = db.relationship("TenantUser", backref=db.backref("tenant"), lazy="dynamic")
    roles = db.relationship(
        "Role",
        secondary=role_to_tenant,
        lazy=True,
        backref=db.backref("tenant", lazy="dynamic"),
    )

    @classmethod
    def find_by_name(self, name):
        return self.query.filter_by(name=name).first()

    def __repr__(self):
        return represent(self, f"{str(self.name)}_{str(self.id)}")


@event.listens_for(Tenant, "after_insert")
def receive_tenant_after_insert(mapper, connection, tenant):
    default_roles = Role.query.filter_by(is_default=True).all()
    if len(default_roles) > 0:
        default_roles = [
            {"role_id": r.id, "tenant_id": tenant.id} for r in default_roles
        ]
        statement = role_to_tenant.insert().values(default_roles)
        db.session.execute(statement)
