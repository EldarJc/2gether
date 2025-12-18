from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from . import db


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseModel(db.Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now
    )
