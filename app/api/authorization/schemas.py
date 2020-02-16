from flask_restplus import fields
from app.data.models.authorization import Permission, Role
from app.schemas import BaseSchema

class PermissionSchema(BaseSchema):
    class Meta:
        fields = ("id", "name")
        model = Permission


class RoleSchema(BaseSchema):
    class Meta:
        fields = ("id", "name", "permissions")
        model = Role
    permissions = fields.Nested(PermissionSchema(many=True))
