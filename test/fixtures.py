import pytest
from app.extensions import app, db
from app import create_app
import os

flask_app = create_app()


@pytest.fixture(scope="function")
def test_client():
    # Boiler Plate
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
    if os.getenv("FLASK_ENV") == "development":
        db.drop_all()
        db.create_all()
    yield testing_client  # this is where the testing happens!

    ctx.pop()
