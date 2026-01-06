import re

from flask_wtf import FlaskForm
from wtforms import EmailField, Field, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from ..utils import get_user
from .auth_service import verify_user


class LoginForm(FlaskForm):
    identifier = StringField(
        "Username or Email",
        validators=[DataRequired(message="Username or Email is required")],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Please enter your password")]
    )
    submit = SubmitField("Log in")

    def validate(self, *args, **kwargs) -> bool:
        is_valid = super(LoginForm, self).validate(*args, **kwargs)

        if not verify_user(self.identifier.data, self.password.data):
            self.form_errors.append("Invalid username/email or password.")
            is_valid = False

        return is_valid


class RegisterForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(message="This field cannot be empty.")]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(message="This field cannot be empty.")]
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="This field cannot be empty."),
            Email(message="Invalid email address format."),
        ],
    )
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="This field cannot be empty."),
            Length(max=50, message="Username cannot be longer than 50 characters."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="This field cannot be empty."),
            Length(min=8, message="Password must have a minimum of 8 characters."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(message="This field cannot be empty.")],
    )
    submit = SubmitField("Sign Up")

    def validate_email(self, field: Field) -> None:
        email = field.data.strip()
        if get_user(email):
            raise ValidationError("This email address is not available")

    def validate_username(self, field: Field) -> None:
        username = field.data.strip()
        if not re.match(r"^\w+$", username):
            raise ValidationError("Username cannot contain special characters.")

        elif get_user(username):
            raise ValidationError("This username is not available")

    def validate(self, *args, **kwargs) -> bool:
        is_valid = super(RegisterForm, self).validate(*args, **kwargs)
        password, confirm_password = self.password.data, self.confirm_password.data

        if confirm_password != password:
            self.confirm_password.errors.append("Passwords do not match.")
            is_valid = False
        return is_valid


class ResetPasswordRequest(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(message="This field cannot be empty.")]
    )
    submit = SubmitField("Get Code")


class ResetPassword(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="This field cannot be empty."),
            Length(min=8, message="Password must have a minimum of 8 characters."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(message="This field cannot be empty.")],
    )
    submit = SubmitField("Reset Password")

    def validate(self, *args, **kwargs) -> bool:
        is_valid = super(ResetPassword, self).validate(*args, **kwargs)
        password, confirm_password = self.password.data, self.confirm_password.data

        if confirm_password != password:
            self.confirm_password.errors.append("Passwords do not match.")
            is_valid = False
        return is_valid
