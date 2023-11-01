import os
from secrets import SystemRandom

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from .db import db
from .jwt.blacklist import BLACKLIST

from .views.store import blp as StoreBlueprint
from .views.item import blp as ItemBlueprint
from .views.tag import blp as TagBlueprint
from .views.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'Stores REST API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.1.0'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DB_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', SystemRandom().getrandbits(256))
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_headers, jwt_payload):
        return jwt_payload['jti'] in BLACKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Invalid access token'}), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Fresh token required'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Invalid access token'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid access token'}), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({'error': 'You need to authorize to access this resource'}), 401

    @app.before_request
    def create_tables():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
