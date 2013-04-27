from flask import request, jsonify, session
import flask.ext.principal as principal
from healingwell.webapp.server.app import app
from models import auth, UserGroup, Group, GroupPermission

principal.Principal(app)

@principal.identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    for record in GroupPermission.select(GroupPermission.permission).join(Group).join(UserGroup).where(UserGroup.user == identity.id):
        identity.provides.add(tuple(record.permission.split(',')))

@app.route("/login", methods=["POST"])
def login():
    user = auth.authenticate(request.form.get("username", ''), request.form.get("password", ''))
    if user:
        auth.login_user(user)
        principal.identity_changed.send(app, identity=principal.Identity(user.id))
        groups = [record.name for record in Group.select(Group.name).join(UserGroup).where(UserGroup.user == user)]
        outcome = {"message": "Logged in.", "redirect_to": request.args.get("next", '/'), "status": "success", "groups": groups}
    else:
        outcome = {"message": "Invalid username or password.", "status": "error"}
    return jsonify(outcome)

@app.route("/logout")
@auth.login_required
def logout():
    user = auth.get_logged_in_user()
    auth.logout_user(user)

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    principal.identity_changed.send(app, identity=principal.AnonymousIdentity())

    return jsonify({"message": "Logged out.", "redirect_to": '/', "status": "success"})
