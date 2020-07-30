from .. import app
from flask import redirect


@app.route('/')
def index():
    return redirect('/index.html')
