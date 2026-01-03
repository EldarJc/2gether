import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, "instance")


class BaseConfig:
    DEBUG = False
    TESTING = False
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")


class DevConfig(BaseConfig):
    SECRET_KEY = os.getenv("DEV_SECRET_KEY")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_DEV_URL") + os.path.join(
        DATABASE_DIR, "app_dev.db"
    )


class TestConfig(BaseConfig):
    SECRET_KEY = os.getenv("TEST_SECRET_KEY")
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TEST_URL") + os.path.join(
        DATABASE_DIR, "app_test.db"
    )
    WTF_CSRF_ENABLED = False


class ProdConfig(BaseConfig):
    pass


LOGGING_LVL = os.getenv("LOGGING_LEVEL", "INFO")
LOGGING_FILE = os.path.join(BASE_DIR, "logs", "app.log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s",
        },
        "detailed": {
            "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "level": LOGGING_LVL,
            "filename": LOGGING_FILE,
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 5,
        },
    },
    "root": {
        "handlers": ["stdout", "file"],
        "level": LOGGING_LVL,
    },
}
