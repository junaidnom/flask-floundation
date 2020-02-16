from app.schemas import BaseSchema
from app.data.models.identity import TenantUser, Tenant
from app.extensions import ma
from app.api.authorization import schemas as authorization_schemas


class TenantUserCreationSchema(BaseSchema):
    class Meta:
        fields = (
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "tenant_id",
            "roles",
        )
        model = TenantUser
        roles = ma.List(ma.Nested(authorization_schemas.RoleSchema))


class TenantUserSchema(BaseSchema):
    class Meta:
        fields = ("id", "username", "first_name", "last_name", "email", "tenant_id")
        model = TenantUser


class TenantSchema(BaseSchema):
    class Meta:
        fields = ("id", "name")
        model = Tenant
