from flask_admin.contrib.sqla import ModelView
from app.data.models.identity import TenantUser
from app.data.models.authorization import Role, Permission
from app.data.models.identity import Tenant
from .extensions import admin, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from app.data.models.talentstat import TestResult

class TestResultView(ModelView):
    column_list = ("id", "name", "result")
    form_columns = ("name", "result")

    def is_accessible(self):
        return current_user.is_authenticated

    def __init__(self, session, **kwargs):
        super(TestResultView, self).__init__(TestResult, session, **kwargs)    


class TenantUserView(ModelView):
    column_list = ("id", "username", "tenant_id", "roles")
    form_choices = {
        "now_showing": [("0", "Not Showing"), ("1", "Showing")],
        "color": [("bw", "Black & White"), ("color", "Color")],
    }

    form_columns = ("username", "email", "password", "tenant", "roles")

    def is_accessible(self):
        return current_user.is_authenticated

    def __init__(self, session, **kwargs):
        super(TenantUserView, self).__init__(TenantUser, session, **kwargs)


class TenantView(ModelView):
    column_list = ("id", "name")
    form_choices = {
        "now_showing": [("0", "Not Showing"), ("1", "Showing")],
        "color": [("bw", "Black & White"), ("color", "Color")],
    }
    form_columns = ("name", "users", "roles")
    column_hide_backrefs = False

    def is_accessible(self):
        return current_user.is_authenticated

    def __init__(self, session, **kwargs):
        super(TenantView, self).__init__(Tenant, session, **kwargs)


class RoleView(ModelView):
    form_choices = {
        "now_showing": [("0", "Not Showing"), ("1", "Showing")],
        "color": [("bw", "Black & White"), ("color", "Color")],
    }
    column_list = ("id", "name", "permissions")
    form_columns = ("name", "permissions")

    def is_accessible(self):
        return current_user.is_authenticated

    def __init__(self, session, **kwargs):
        super(RoleView, self).__init__(Role, session, **kwargs)


class PermissionView(ModelView):
    form_choices = {
        "now_showing": [("0", "Not Showing"), ("1", "Showing")],
        "color": [("bw", "Black & White"), ("color", "Color")],
    }
    column_list = ("id", "name")
    form_columns = ("name", "roles")

    def is_accessible(self):
        return current_user.is_authenticated

    def __init__(self, session, **kwargs):
        super(PermissionView, self).__init__(Permission, session, **kwargs)



def register_views():
    # Register admin view
    admin.add_view(TenantUserView(db.session, category="Identity"))
    admin.add_view(TenantView(db.session, category="Identity"))

    admin.add_view(RoleView(db.session, category="Authorization"))
    admin.add_view(PermissionView(db.session, category="Authorization"))

    admin.add_view(TestResultView(db.session, category="TestResult"))
