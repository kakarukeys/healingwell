from flask import Flask
from healingwell.webapp.server import configs

app = Flask(__name__)
app.config.from_object(configs)

if app.config['DEBUG']: #serve static files when developing
    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/': os.path.join(os.path.dirname(__file__), '../client/app')})

if __name__ == '__main__':
    from auth.views import *
    app.run()
    