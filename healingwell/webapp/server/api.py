from flask_peewee.rest import RestAPI, RestResource
from flask.ext.principal import Permission
from flask_peewee.rest import Authentication

from healingwell.webapp.server.app import app


api = RestAPI(app, default_auth=Authentication(protected_methods=[]))

class RestrictedAccessResource(RestResource):
    def __init__(self, rest_api, model, *args, **kwargs):
        super(RestrictedAccessResource, self).__init__(rest_api, model, *args, **kwargs)
        self.permissions = [Permission((model.__name__, action)) for action in ("create", "read", "update", "delete")]

    def check_post(self, obj=None):
        return self.permissions[0].can()

    def check_get(self, obj=None):
        return self.permissions[1].can()

    def check_put(self, obj):
        return self.permissions[2].can()

    def check_delete(self, obj):
        return self.permissions[3].can()
