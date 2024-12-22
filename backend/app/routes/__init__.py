from flask import Flask
from .auth import bp as auth_bp
from .main import bp as main_bp
from .product import bp as product_bp


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
