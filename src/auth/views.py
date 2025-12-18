from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug import Response

from ..utils import find_user
from . import auth_bp
from .auth_utils import (
    create_user,
    send_reset_email,
    update_password,
    verify_token,
)
from .forms import LoginForm, RegisterForm, ResetPassword, ResetPasswordRequest


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    if current_user.is_anonymous:
        form = LoginForm()
        if request.method == "POST" and form.validate_on_submit():
            user = find_user(form.email_username.data)
            login_user(user)
            return redirect("/home")
        return render_template("auth/login.html", form=form)

    return redirect("/home")


@auth_bp.route("/logout")
@login_required
def logout() -> Response:
    logout_user()

    return redirect("/home")


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> Response | str:
    if current_user.is_anonymous:
        form = RegisterForm()
        if form.validate_on_submit():
            user = create_user(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
            )

            login_user(user)
            flash("Registration successful.", "success")
            return redirect("/home")
        return render_template("auth/register.html", form=form)

    return redirect("/home")


@auth_bp.route("/password-reset-request", methods=["GET", "POST"])
def reset_request() -> Response | str:
    if current_user.is_anonymous:
        form = ResetPasswordRequest()
        if form.validate_on_submit():
            send_reset_email(form.email.data)
            flash(
                "If an account exists with this email, a reset link has been sent.",
                "info",
            )
            return redirect("/home")

        return render_template("auth/request_token.html", form=form)

    return redirect("/home")


@auth_bp.route("/password-reset/<token>", methods=["GET", "POST"])
def password_reset(token: str) -> Response | str:
    if current_user.is_anonymous:
        form = ResetPassword()

        user_id = verify_token(token)
        if not user_id:
            flash("Invalid or expired token.", "error")
            return redirect(url_for("auth.reset_request"))

        elif request.method == "POST" and form.validate_on_submit():
            if update_password(user_id, form.password.data):
                flash("Your password has been reset!", "success")
                return redirect(url_for("auth.login"))

            flash("Error while resetting your password.", "danger")
            return redirect(url_for("auth.login"))

        return render_template("auth/password_reset.html", form=form)

    return redirect("/home")
