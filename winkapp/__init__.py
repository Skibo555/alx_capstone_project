from flask import Flask
from routes.posts import post_pages


def create_app():
    app = Flask(__name__)
    app.register_blueprint(post_pages)

    return app
