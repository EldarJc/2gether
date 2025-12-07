from flask import Flask

def create_app(config):
    if config is None:
        raise ValueError("Configuration is required but was not provided.")

    app = Flask(__name__)
    app.config.from_object(config)

    return app