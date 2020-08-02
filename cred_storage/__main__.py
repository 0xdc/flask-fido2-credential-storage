from .wsgi import app

app.run(ssl_context="adhoc", debug=True)
