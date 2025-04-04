# backend/app.py

"""
Main application module for the Goodbooks API
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from backend.config import config_by_name, config

# initialize the SQLAlchemy instance
db = SQLAlchemy()

# initialize JWT Manager
jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_loader(identity):
    """Convert user identity to a JSON serializable format"""
    return identity

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Extract user identity from JWT data"""
    return jwt_data['sub']

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"success": False, "message": "Invalid token", "error": str(error)}), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"success": False, "message": "No authorization token provided"}), 401

def create_app(config_name=None):
    """Factory function to create and configure Flask application"""

    # use environment variable if config_name not provided
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'development')

    # create Flask app
    app = Flask(__name__)

    # load configuration
    app.config.from_object(config_by_name[config_name])

    # enable CORS
    CORS(app)

    # initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)

    # register blueprints
    from backend.api.routes import register_routes
    register_routes(app)

    # create database tables if they don't exist
    with app.app_context():
        # ensure database directory exists
        db_path = Path(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        db_dir = db_path.parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        db.create_all()

    return app

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(debug=config.DEBUG)