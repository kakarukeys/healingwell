from flask import Flask, request, jsonify
from flask_peewee.auth import Auth
from flask_peewee.db import Database

import configs

app = Flask(__name__)
app.config.from_object(configs)

db = Database(app)
auth = Auth(app, db)

@app.route("/login", methods=["POST"])
def login():
    user = auth.authenticate(request.form.get("username", ''), request.form.get("password", ''))
    if user:
        auth.login_user(user)
        outcome = {"message": "Logged in.", "redirect_to": request.args.get("next", '/')}, 302
    else:
        outcome = {"message": "Invalid username or password."}, 200
    response = jsonify(**outcome[0])
    response.status_code = outcome[1]
    return response

@app.route("/logout")
@auth.login_required
def logout():
    user = auth.get_logged_in_user()
    auth.logout_user(user)
    response = jsonify(message="Logged out.", redirect_to='/')
    response.status_code = 302
    return response

if app.config['DEBUG']: #serve static files when developing
    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/': os.path.join(os.path.dirname(__file__), '../client/app')})

if __name__ == '__main__':
    app.run()
    