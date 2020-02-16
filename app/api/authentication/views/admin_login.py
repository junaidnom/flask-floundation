from flask import make_response, redirect, render_template, request

from flask.views import View
from flask_restplus import Resource, fields
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, fields
from wtforms.validators import DataRequired

from app.api.api import api
from app.api.authentication.services import authentication_service
from app.common.http import request_response_codes


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class LoginView(Resource):
    def get(self):
        header = {"Content-Type": "text/html"}
        form = LoginForm()
        return make_response(render_template("login.html", form=form), 200, header)

    @api.doc(responses=request_response_codes())
    def post(self):
        header = {"Content-Type": "text/html"}
        form = LoginForm()
        if form.validate_on_submit():
            is_authed = authentication_service.login_admin(
                form.username.data, form.password.data
            )
            if is_authed:
                return redirect("/api/v1/admin")
            else:
                abort(401, "Nope")
        return abort(401, "Nope")
