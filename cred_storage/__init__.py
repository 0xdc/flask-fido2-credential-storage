import os
import click
from flask import Flask, cli


def create_app(test_config=None):
    app = Flask(__name__, static_url_path="", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(32),
        DATABASE=os.environ.get("CREDSTORE_DATABASE", "sqlite:///db.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.cfg', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from .database import db_session, init_db

        from . import views  # noqa E402 F401
        from .views import fido2  # noqa E402 F401

        init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()


    @app.cli.add_command
    @click.command('init-db')
    @cli.with_appcontext
    def init_db_command():
        click.echo("initialising the database tables")
        init_db()

    return app
