from flask import request, jsonify
from healingwell.webapp.server.app import app
from models import auth

@app.route("/login", methods=["POST"])
def login():
    user = auth.authenticate(request.form.get("username", ''), request.form.get("password", ''))
    if user:
        auth.login_user(user)
        outcome = {"message": "Logged in.", "redirect_to": request.args.get("next", '/'), "status": "success"}
    else:
        outcome = {"message": "Invalid username or password.", "status": "error"}
    return jsonify(outcome)

@app.route("/logout")
@auth.login_required
def logout():
    user = auth.get_logged_in_user()
    auth.logout_user(user)
    return jsonify({"message": "Logged out.", "redirect_to": '/', "status": "success"})
