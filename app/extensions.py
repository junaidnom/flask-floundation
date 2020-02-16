import os

from flask import Flask, url_for
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api
from flask_admin import Admin, AdminIndexView
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
CORS(app)

admin = Admin(
    app, name="Demo Admin", template_mode="bootstrap3", url="/api/v1/admin"
)

db = SQLAlchemy(session_options={"autocommit":False, "autoflush": False})
migrate = Migrate(app, db)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
login = LoginManager(app)
