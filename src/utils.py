from .database import db
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
    return db.session.get(User, user_id)


def set_attributes(instance: object, attributes: dict) -> None:
    for key, value in attributes.items():
        if hasattr(type(instance), key):
            setattr(instance, key, value)


def save_instance(instance: object) -> bool:
    try:
        db.session.add(instance)
        db.session.commit()
        return True

    except Exception:
        db.session.rollback()
        return False


def update_instance(instance: object, attributes: dict) -> bool:
    set_attributes(instance, attributes)
    if db.session.is_modified(instance) or instance not in db.session:
        return save_instance(instance)

    return False


def update_password(user_id: int, new_password: str) -> bool:
    user = get_user_by_id(user_id)
    if not user:
        return False
    return update_instance(user, {"password": new_password})
