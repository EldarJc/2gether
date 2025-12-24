from flask import Blueprint

user_bp = Blueprint("user", __name__)
account_bp = Blueprint("account", __name__, url_prefix="/account")
user_bp.register_blueprint(account_bp)

from . import views
