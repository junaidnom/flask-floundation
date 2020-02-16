from flask import Blueprint
from flask_restplus import Api

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

authorization_doc = {
    "apikey": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(
    api_blueprint,
    doc="/swagger/",
    authorizations=authorization_doc,
    version="0.0.1",
    title="Demo",
    description="Flask F1 Demo",
)

# NOTE: Namespace dependencies must be imported inline
from app.api.identity.routes import ns as identity_ns
from app.api.authentication.routes import ns as authentication_ns

api.add_namespace(identity_ns)
api.add_namespace(authentication_ns)
