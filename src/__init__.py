from flask import Flask

from src.extensions import login_manager, mail


def create_app(config: type) -> Flask:
    if config is None:
        raise ValueError("Application configuration is missing")

    app = Flask(__name__, template_folder="ui/templates")
    app.config.from_object(config)

    from .database import db, db_migrate

    db.init_app(app)
    db_migrate.init_app(app, db)

    login_manager.init_app(app)
    mail.init_app(app)

    from .auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
