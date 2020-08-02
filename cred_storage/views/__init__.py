from flask import redirect, current_app


@current_app.route('/')
def index():
    return redirect('/index.html')
