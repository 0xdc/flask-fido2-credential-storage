from . import app
from .database import init_db

init_db()
app.run(ssl_context="adhoc", debug=True)
