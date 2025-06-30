from flask import Flask
from flasgger import Swagger
from .routes import bp as main_bp
def create_app():
    app = Flask(__name__)
    Swagger(app)

    app.register_blueprint(main_bp)

    return app