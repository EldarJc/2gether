from .database.models import User


def find_user_by_email(email: str) -> User | None:
    return User.query.filter_by(email=email).first()


def find_user_by_username(username: str) -> User | None:
    return User.query.filter_by(username=username).first()


def find_user(identifier: str) -> User | None:
    if "@" in identifier:
        return find_user_by_email(identifier)

    return find_user_by_username(identifier)


def get_user_by_id(user_id: int) -> User | None:
    return User.query.get(user_id)
