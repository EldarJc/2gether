from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug import Response

from ..utils import find_user_by_username, update_instance
from . import account_bp, user_bp
from .forms import CredentialsUpdateForm, UpdateProfileForm


@account_bp.route("/update", methods=["GET", "POST"])
@login_required
def profile_update() -> Response | str:
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        is_updated = update_instance(
            current_user,
            {
                "first_name": form.first_name.data.strip(),
                "last_name": form.last_name.data.strip(),
                "username": form.username.data.strip(),
            },
        )
        if is_updated:
            flash("Your profile has been updated!", "success")

            return redirect(
                url_for("user.account.profile_update"),
                code=303,
            )

        flash("Please check your profile details", "error")
    return render_template("user/profile_update.html", form=form)


@account_bp.route("/security", methods=["GET", "POST"])
@login_required
def security_update() -> Response | str:
    form = CredentialsUpdateForm(obj=current_user)
    if form.validate_on_submit():
        is_updated = update_instance(
            current_user,
            {
                "email": form.email.data.strip(),
                "password": form.password.data,
            },
        )

        if is_updated:
            flash("Your profile has been updated!", "success")
            return redirect(
                url_for("user.account.security_update"),
                code=303,
            )

    return render_template("user/security_update.html", form=form)


@user_bp.route("/<string:username>")
def profile(username: str) -> Response | str:
    user = find_user_by_username(username)

    if not user:
        abort(404, description=f"User {username} not found.")

    return render_template("user/profile.html", user=user)
