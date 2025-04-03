# backend/config.py

"""
Configuration settings for the backend API
"""

import os
from pathlib import Path

# base directory is backend root
BASE_DIR = Path(__file__).resolve().parent

# get environment or default to development
ENV = os.environ.get('FLASK_ENV', 'development')

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # database - reuse the same DB connection from ETL pipeline
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        f'sqlite:///{Path(__file__).resolve().parent.parent / "database" / "goodbooks.db"}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 3600 # 1 hour

    # API settings
    API_TITLE = 'Goodbooks API'
    API_VERSION = 'v1'
    API_DESCRIPTION = 'An API for Goodbooks book recommendation system'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # use environment variable for database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', Config.SQLALCHEMY_DATABASE_URI)
    # use environment variable for secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-needs-better-secret'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY

# config dictionary to select config based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# get configuration class by environment name
config = config_by_name[ENV]