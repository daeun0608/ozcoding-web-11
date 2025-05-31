from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    Swagger(app)  # Swagger 초기화

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app