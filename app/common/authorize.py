from functools import wraps
from flask import request, abort
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from app.data.models import identity
from collections.abc import Iterable
from app.data.models.authorization import PermissionType
from app.extensions import db


def get_claims_user():
    try:
        claims = get_jwt_claims()
        claims_user = identity.TenantUser.query.filter_by(id=claims["id"]).first()
        return claims_user
    except Exception:
        abort(401, "Malformed Claims Request")


class Authorize:
    def __init__(self, permissions):
        self.permissions = permissions
        self.claims_user = None
        self.authorized = False

    def authorize(self):
        if self.claims_user == None:
            abort(401, "Missing Claims User")

        # NOTE: This is a nested loop but because of the data definition
        # it will only need to do one query.
        pids = [
            PermissionType(permission.name)
            for role in self.claims_user.roles
            for permission in role.permissions
        ]

        # NOTE: Convert singles into lists for comparison
        self.permissions = [
            [permission] if not isinstance(permission, Iterable) else permission
            for permission in self.permissions
        ]

        # NOTE: Check to see if any combination of the pids provided match
        # permissions assigned to the endpoint.
        self.authorized = any(
            [set(permission).issubset(pids) for permission in self.permissions]
        )

    def __call__(self, fn, *args, **kwargs):
        def wrapper(*args, **kwargs):
            self.claims_user = get_claims_user()

            """
            Currently this method will query the database to retreive
            information about a users permissions.
            However, we should strcuture it to query redis
            Before moving this into production.
            """

            self.authorize()

            if not self.authorized:
                abort(403, "Insufficent Permissions")

            return fn(*args, **kwargs)

        return wrapper
