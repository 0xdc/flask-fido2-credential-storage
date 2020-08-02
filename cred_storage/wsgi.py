from . import create_app

app = create_app()

with app.app_context():
    from . import views  # noqa F401
    from .views import fido2  # noqa F401
    from .database import init_db

    init_db()
