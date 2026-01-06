from flask import current_app as app
from flask import url_for
from flask_mail import Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from ..extensions import mail
from ..utils import get_user


def verify_user(identifier: str, password: str) -> bool:
    user = get_user(identifier)

    if user and user.check_password(password):
        return True

    return False


def request_token(user_id: int) -> str | None:
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    data = {
        "user_id": user_id,
    }
    return serializer.dumps(data)


def verify_token(token: str, expires_in: int = 600) -> int | None:
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        data = serializer.loads(token, max_age=expires_in)
        return data["user_id"]

    except (SignatureExpired, BadSignature):
        return None


def send_reset_email(user_email: str) -> None:
    user = get_user(user_email)

    if not user:
        return

    token = request_token(user.id)
    reset_url = url_for("auth.password_reset", token=token, _external=True)

    msg = Message("Reset password instruction", recipients=[str(user.email)])

    msg.body = f"""Hello {user.username},

        Someone has requested a link to change your password, and you can do this through the link below.

            {reset_url}

        If you didn't request this, please ignore this email.

        Your password won't change until you access the link above and create a new one.
        """

    mail.send(msg)
