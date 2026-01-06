from functools import wraps

from flask import redirect
from flask_login import current_user

MAIN_URL = "/"  # change later


def anonymous_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(MAIN_URL)

        return func(*args, **kwargs)

    return decorated_view
