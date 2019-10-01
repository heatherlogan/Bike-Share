import os
from flask import Flask
from flask_ripozo import FlaskDispatcher
from ripozo.adapters.hal import HalAdapter
from asterix import component
from flask_jwt import JWT
from commons.auth import (
    authenticate, payload_handler, identity
)
from py2neo import Graph
from flask_cors import CORS, cross_origin


def get_config():
    from config import config
    return config[os.getenv('APP_CONFIG', 'dev')]


def create_ripozo(app):
    return FlaskDispatcher(app, url_prefix="/api")


def register_resources(ripozo):
    from users.api_v1 import (
        ClientResource, UserResource, ProviderResource,
        ScopeResource
    )
    ripozo.register_adapters(HalAdapter)
    ripozo.register_resources(
      UserResource, ClientResource, ProviderResource, ScopeResource
    )


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def create_jwt(app):
    jwt = JWT(app, authenticate, identity)
    jwt.jwt_payload_handler(payload_handler)


def start_cors(app):
    CORS(app, resources={r'/api/*': {'origins': '*'}})


def create_py2neo(config):
    return Graph()


def sanitize(config):
    import os
    if config.DEBUG:
        open(os.path.expanduser("~/.neo4j/known_hosts"), "w").close()

components = {
    "components": {
        "config": component(set(), get_config),
        "app": component({"config", }, create_app),
        "ripozo": component({"app", }, create_ripozo),
        "jwt": component({"app", }, create_jwt),
        "neo4j": component({"config", }, create_py2neo)
    },
    "hooks": [register_resources, start_cors],
    "bind_to": "app"
}
