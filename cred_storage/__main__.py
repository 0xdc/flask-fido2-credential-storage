from . import create_app
from .database import init_db

app = create_app()
app.run(ssl_context="adhoc", debug=True)
