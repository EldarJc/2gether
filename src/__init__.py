from flask import Flask

from .database import db, db_migrate

def create_app(config):
    if config is None:
        raise ValueError("Configuration is required but was not provided.")

    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    db_migrate.init_app(app, db)

    return app