from datetime import timedelta
from uuid import uuid4

from flask import abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.common.http import ResponseCodesEnum, generic_response
from app.data.models import identity


def login_admin(username, password):
    _current_user = identity.TenantUser.find_by_username(username=username)
    if _current_user:
        is_authed = check_password_hash(_current_user._password, password)
        if is_authed:
            login_user(_current_user)
            return True
    abort(ResponseCodesEnum.Unauthorized.value, "Unauthorized")


def login(login_schema):
    current_user = identity.TenantUser.find_by_username(login_schema["username"])
    if current_user:
        is_authed = check_password_hash(
            current_user._password, login_schema["password"]
        )
        if is_authed:
            access_token = create_access_token(
                identity=current_user, expires_delta=timedelta(minutes=120)
            )
            refresh_token = create_refresh_token(identity=current_user)
            return {"access_token": access_token, "refresh_token": refresh_token}
    abort(ResponseCodesEnum.Unauthorized.value, "Username or Password is incorrect")


"""
We can use the get_jwt_identity() function to get the identity of
the refresh token, and use the create_access_token() function again
to make a new access token for this identity.
"""


def refresh(refresh_token):
    current_user = get_jwt_identity()
    new_token = {"access_token": create_access_token(identity=current_user)}
    return new_token
