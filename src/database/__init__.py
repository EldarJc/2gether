from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


from .models import (
    Event,
    EventAttendee,
    Group,
    GroupMember,
    Location,
    Tag,
    User,
    event_tags,
    group_tags,
)

__all__ = [
    "User",
    "Group",
    "Event",
    "Tag",
    "Location",
    "GroupMember",
    "EventAttendee",
    "group_tags",
    "event_tags",
]
