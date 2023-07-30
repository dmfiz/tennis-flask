from os import environ, path
#from dotenv import load_dotenv


# Specificy a `.env` file containing key/value config values
#basedir = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(basedir, ".env"))


# General Config
ENVIRONMENT = environ.get("ENVIRONMENT")
FLASK_APP = environ.get("FLASK_APP")
FLASK_DEBUG = environ.get("FLASK_DEBUG")
#SECRET_KEY = environ.get("SECRET_KEY")
#SECURITY_PASSWORD_SALT = environ.get("SECURITY_PASSWORD_SALT")

SECRET_KEY = "SecretSaucedChicken"
SECURITY_PASSWORD_SALT = "SecretSaltyChicken"


class BaseConfig(object):
    """Base configuration."""


    # main config
    SESSION_TYPE = "filesystem"
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

