from flask import render_template

from . import error_bp


@error_bp.app_errorhandler(404)
def not_found(error):
    msg = getattr(error, "description")
    return render_template("errors/404.html", msg=msg), 404
