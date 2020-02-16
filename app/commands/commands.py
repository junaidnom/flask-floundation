from app.extensions import app
from app.extensions import db
from flask.cli import with_appcontext
import click
import os
from pathlib import Path
from app.api.identity.services import tenant_service, tenant_user_service
from app.data.models import identity
from app.data.models import authorization
from app.common.utils import get_or_create
from app.data.register import *
import pathlib
from google.cloud import storage
from app.common.utils import upload_blob
import app.common.authorize
from app.common import data


@click.command()
@click.argument("image_name")
@click.option(
    "--publish", is_flag=True, prompt="Would you like to publish?", hide_input=False
)
@with_appcontext
def drawerd(image_name, publish):
    """
        Generates ERD in /temp/<image_name>
    """
    # TODO : add publishing functionality once GCP access is setup
    from eralchemy import render_er

    pathlib.Path("temp").mkdir(parents=True, exist_ok=True)
    render_er(db.Model, os.path.join("temp", image_name))
    print(f"Diagram created : {os.path.join(os.path.curdir, 'temp', image_name)}")
    if publish:
        upload_blob("<your_bucket_goes_here>", f"temp/{image_name}", "erd.png")


@click.command()
@with_appcontext
def seed():
    """
    Basic setup for admin user and base roles and permissions.
    """
    data.seed()


@click.command()
@click.argument("new_ns")
@with_appcontext
def createdomain(new_ns):
    """
    This method is used to generate new domains inside the api
    """
    p = os.path.join(os.path.abspath(os.curdir), "app/api")
    new_domain = os.path.join(p, new_ns)
    if os.path.exists(new_domain):
        raise Exception(f"Domain exists : {new_ns}")
    resources = os.path.join(new_domain, "resources")
    services = os.path.join(new_domain, "services")
    os.makedirs(new_domain)
    os.makedirs(services)
    os.makedirs(resources)
    open(f"{resources}/{new_ns}_resource.py", "w+")
    open(f"{services}/{new_ns}_service.py", "w+")
    open(f"{new_domain}/routes.py", "w+")
    open(f"{new_domain}/schemas.py", "w+")


@click.command()
@click.argument("new_role")
@with_appcontext
def createdefaultrole(new_role):
    role = get_or_create(db.session, Role, name=new_role, is_default=True)
    tenants = identity.Tenant.query.all()
    for tenant in tenants:
        role_assignment_exists = next(
            (r for r in tenant.roles if r.id == role.id), None
        )
        if not role_assignment_exists:
            tenant.roles.append(role)
            db.session.add(tenant)
    db.session.commit()
    return role


def register_commands(app):
    app.cli.add_command(createdomain)
    app.cli.add_command(seed)
    app.cli.add_command(drawerd)
    app.cli.add_command(createdefaultrole)
