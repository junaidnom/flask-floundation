from app.data.models import identity
from app.data.models import authorization
from app.common.utils import get_or_create
from app.data.register import *
from app.extensions import db


def seed():
    """
    Basic setup for admin user and base roles and permissions.
    """

    permissions = [
        get_or_create(db.session, authorization.Permission, name=permission.value)
        for permission in authorization.PermissionType
    ]

    admin_role = get_or_create(
        db.session,
        authorization.Role,
        name=authorization.RoleDefaultType.ADMIN.value,
        is_default=True,
    )

    readonly_role = get_or_create(
        db.session,
        authorization.Role,
        name=authorization.RoleDefaultType.READONLY.value,
        is_default=True,
    )

    for permission in permissions:
        exists = (
            db.session.query(authorization.role_to_permission)
            .filter_by(permission_id=permission.id, role_id=admin_role.id)
            .first()
        )
        if not exists:
            statement = authorization.role_to_permission.insert().values(
                role_id=admin_role.id, permission_id=permission.id
            )
            db.session.execute(statement)
            db.session.commit()

    tenant = get_or_create(db.session, identity.Tenant, name="TestCo")

    tenant_user = (
        db.session.query(identity.TenantUser).filter_by(username="admin").first()
    )

    if not tenant_user:
        tenant_user = get_or_create(
            db.session,
            identity.TenantUser,
            username="admin",
            password="1234",
            tenant_id=tenant.id,
        )
        roles = Role.query.all()
        for role in roles:
            tenant_user.roles.append(role)
    db.session.commit()
