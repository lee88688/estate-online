from flask import Flask
from .api import bp as api_bp


def create_app():
    app = Flask(__name__, static_folder='static')

    app.register_blueprint(api_bp)

    return app
