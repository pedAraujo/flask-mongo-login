from flask import Flask

from .routes import main
from .auth import auth


def create_app():
    server = Flask(__name__)
    server.config.from_pyfile("config.py")
    server.register_blueprint(main)
    server.register_blueprint(auth)

    return server
