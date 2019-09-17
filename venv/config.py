"""App configuration."""
from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = "oijas21ijd99fghOUOHuy0109ubOUByusa08108nSOu0hasf01081naslknfd081803"  # os.urandom(24)
    SESSION_TYPE = 'filesystem'
    FLASK_APP = "app"
    #FLASK_ENV = "environ.get('FLASK_ENV')"

    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')


