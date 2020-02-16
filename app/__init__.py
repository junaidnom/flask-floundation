import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy


def create_app():
    from .extensions import app

    # Set environment variables
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FLASK_ADMIN_SWATCH"] = "superhero"

    # Connect application to database
    from .extensions import db

    db.init_app(app)

    # Register click commands
    from .commands.commands import register_commands

    register_commands(app)

    # Add api v1
    from .api.api import api_blueprint

    app.register_blueprint(api_blueprint)

    # Register all data models so they can be migrated
    from .data import register

    # Register admin views
    from .admin import register_views

    register_views()

    return app
