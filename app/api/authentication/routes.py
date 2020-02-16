from flask import Blueprint, jsonify, url_for
from flask_restplus import Api, Resource, reqparse
from app.api.api import api
from app.api.authentication.resources.authenticate import Login, Refresh
from app.api.authentication.views.admin_login import LoginView

# NOTE: Define namespace for route scoping
ns = api.namespace("authentication", description="Authentication Endpoints")


api.add_resource(LoginView, "/admin/login")

ns.add_resource(Login, "/login")
ns.add_resource(Refresh, "/refresh")
