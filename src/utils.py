from .database import User


def get_user(identifier=None) -> User | None:
    if not identifier:
        return None

    if "@" in identifier:
        return User.query.filter_by(email=identifier).first()

    return User.query.filter_by(username=identifier).first()
