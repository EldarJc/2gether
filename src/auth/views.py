from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug import Response

from ..database.models import User
from ..decorators import anonymous_required
from ..utils import get_user
from . import auth_bp
from .auth_service import send_reset_email, verify_token
from .forms import LoginForm, RegisterForm, ResetPassword, ResetPasswordRequest


@auth_bp.route("/login", methods=["GET", "POST"])
@anonymous_required
def login() -> Response | str:
    form = LoginForm()

    if form.validate_on_submit():
        user = get_user(form.identifier.data.strip())

        login_user(user)
        return redirect("/home")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout() -> Response:
    logout_user()

    return redirect("/home")


@auth_bp.route("/register", methods=["GET", "POST"])
@anonymous_required
def register() -> Response | str:
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.create(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=form.email.data.strip(),
            username=form.username.data.strip(),
            password=form.password.data,
        )

        login_user(user)
        flash("Registration successful.", "success")
        return redirect("/home")

    return render_template("auth/register.html", form=form)


@auth_bp.route("/password-reset-request", methods=["GET", "POST"])
@anonymous_required
def reset_request() -> Response | str:
    form = ResetPasswordRequest()

    if form.validate_on_submit():
        send_reset_email(form.email.data.strip())
        flash(
            "If an account exists with this email, a reset link has been sent.",
            "info",
        )
        return redirect("/home")

    return render_template("auth/request_token.html", form=form)


@auth_bp.route("/password-reset/<token>", methods=["GET", "POST"])
@anonymous_required
def password_reset(token: str) -> Response | str:
    form = ResetPassword()
    user_id = verify_token(token)

    if not user_id:
        flash("Invalid or expired token.", "error")
        return redirect(url_for("auth.reset_request"))

    if form.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        user.update(password=form.password.data)

        flash("Your password has been reset!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/password_reset.html", form=form)
