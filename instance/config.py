from os import environ, getenv, path
from dotenv import load_dotenv


# Specificy a `.env` file containing key/value config values
basedir = path.expanduser("~/tennis-flask")
load_dotenv(path.join(basedir, ".env"))

# General Config
ENVIRONMENT = environ.get("ENVIRONMENT")
FLASK_APP = environ.get("FLASK_APP")
FLASK_DEBUG = environ.get("FLASK_DEBUG")
SECRET_KEY = getenv("SECRET_KEY")
SECURITY_PASSWORD_SALT = getenv("SECURITY_PASSWORD_SALT")

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_TRACK_MODIFICATIONS = False



class BaseConfig(object):
    """Base configuration."""


    # main config
    SESSION_TYPE = "filesystem"
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

