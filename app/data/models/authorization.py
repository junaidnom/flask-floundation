from sqlalchemy import text as sa_text
from sqlalchemy.ext.hybrid import hybrid_property

from app.common.utils import represent
from app.extensions import db
from app.schemas import BaseSchema
import enum
from marshmallow import fields


class RoleDefaultType(enum.Enum):
    ADMIN = "admin"
    READONLY = "readonly"

class PermissionType(enum.Enum):
    CAN_READ_TENANT_USER = "can_read_tenant_user"
    CAN_CREATE_TENANT_USER = "can_create_tenant_user"
    CAN_CREATE_ALL_TENANT_USERS = "can_create_all_tenant_users"
    CAN_READ_TENANT = "can_read_tenant"
    CAN_CREATE_TENANT = "can_create_tenant"
    CAN_READ_ALL_TENANTS = "can_read_all_tenants"
    CAN_READ_ALL_TENANT_USERS = "can_read_all_tenant_users"


role_to_permission = db.Table(
    "role_to_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permission.id"),
        primary_key=True,
        index=True,
    ),
)

role_to_tenant_user = db.Table(
    "role_to_tenant_user",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
    db.Column(
        "tenant_user_id", db.Integer, db.ForeignKey("tenant_user.id"), primary_key=True
    ),
)

role_to_tenant = db.Table(
    "role_to_tenant",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
    db.Column("tenant_id", db.Integer, db.ForeignKey("tenant.id"), primary_key=True),
)


class Role(db.Model):
    """This table acts as the highest level of permissioning inside the
        application. Each role is to be directly assigned to a user and
        consists of Permissions. Each User can have many Roles.
    """

    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    is_default = db.Column(db.Boolean, default=False)
    permissions = db.relationship(
        "Permission",
        secondary=role_to_permission,
        lazy=False,
        backref=db.backref("roles", lazy=False),
    )

    def __repr__(self):
        return represent(self, self.name)


class Permission(db.Model):
    """Permissions are the smallest level of authorization provided and
        are used to directly control access to components and endpoints.
    """

    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)

    def __repr__(self):
        return represent(self, self.name)


