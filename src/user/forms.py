from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.fields import Field, StringField
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length,
    Optional,
    ValidationError,
)

from ..utils import find_user_by_email, find_user_by_username


class UpdateProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=40)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=40)])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=50)]
    )
    submit = SubmitField("Update Profile")

    def validate_username(self, field: Field) -> None:
        username = field.data.strip()

        if username != current_user.username and find_user_by_username(username):
            raise ValidationError("This username address is not available")


class CredentialsUpdateForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(max=254)])
    current_password = PasswordField("Current Password", validators=[Optional()])
    new_password = PasswordField("New Password", validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm New Password", validators=[Optional(), EqualTo("new_password")]
    )
    submit = SubmitField("Update Credentials")

    def validate_email(self, field: Field) -> None:
        email = field.data.strip()

        if email != current_user.email.strip() and find_user_by_email(email):
            raise ValidationError("This email address is not available")

    def validate_current_password(self, field: Field) -> None:
        password = field.data

        if password and not current_user.check_password(password):
            raise ValidationError("Incorrect password.")

    def validate(self, *args, **kwargs) -> bool:
        is_valid = super(CredentialsUpdateForm, self).validate(*args, **kwargs)

        if not is_valid:
            return is_valid

        current_password = self.current_password
        new_password = self.new_password
        confirm_password = self.confirm_password

        if new_password.data and confirm_password.data:
            if not current_password.data:
                current_password.errors.append("Please enter current password")
                is_valid = False

            elif new_password.data == current_password.data:
                new_password.errors.append("Current password is same.")
                is_valid = False

        return is_valid
