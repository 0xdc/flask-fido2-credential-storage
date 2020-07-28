import os

import click
from flask import Flask, cli

from .database import db_session

app = Flask(__name__, static_url_path="")
app.secret_key = os.urandom(32)

from . import views
from .views import fido2

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.cli.add_command
@click.command('init-db')
@cli.with_appcontext
def init_db_command():
    click.echo("initialising the database tables")
    from .database import init_db
    init_db()

