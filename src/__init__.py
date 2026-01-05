import logging.config

from flask import Flask

from config import LOGGING

from .database import db, migrate
from .extensions import login_manager, mail


def create_app(config_name=None) -> Flask:
    app = Flask(__name__)
    if config_name is None:
        raise ValueError("config_name must be provided")

    app.config.from_object(config_name)

    logging.config.dictConfig(LOGGING)

    mail.init_app(app)
    login_manager.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
