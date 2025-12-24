from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from src.extensions import mail

from ..database.models import User
from ..utils import find_user_by_email, update_instance


def create_user(
    username: str, first_name: str, last_name: str, email: str, password: str
) -> User | None:
    new_user = User()

    if update_instance(
        new_user,
        {
            "username": username.strip(),
            "email": email.strip(),
            "password": password,
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
        },
    ):
        return new_user

    return None


def request_token(user_id: int) -> str | None:
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    data = {
        "user_id": user_id,
    }
    return serializer.dumps(data)


def verify_token(token: str, expires_in: int = 600) -> int | None:
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        data = serializer.loads(token, max_age=expires_in)
        return data["user_id"]

    except SignatureExpired:
        return None
    except BadSignature:
        return None


def send_reset_email(user_email: str) -> None:
    user = find_user_by_email(user_email)
    if user:
        token = request_token(user.id)
        msg = Message("Reset password instruction", recipients=[str(user.email)])
        msg.body = f"""
            Hello {user.username}

            Someone has requested a link to change your password, and you can do this through the link below.

                {url_for("auth.password_reset", token=token, _external=True)}

            If you didn't request this, please ignore this email.

            Your password won't change until you access the link above and create a new one.
        """
        mail.send(msg)
