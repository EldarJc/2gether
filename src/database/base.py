from datetime import datetime, timezone
from typing import Self

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column

from . import db


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CRUDMixin(object):
    """Mixin with basic methods (create, update, soft_delete and delete) for models."""

    def _set_attributes(self, **kwargs) -> None:
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except IntegrityError as e:
            db.session.rollback()
            raise e

    @classmethod
    def create(cls, **kwargs) -> Self:
        instance = cls()
        instance._set_attributes(**kwargs)

        return instance.save()

    def update(self, **kwargs) -> Self:
        if self.is_deleted:
            raise ValueError("Cannot update a deleted object")

        self._set_attributes(**kwargs)
        return self.save()

    def soft_delete(self) -> Self:
        if self.is_deleted:
            raise ValueError("Object is already soft deleted")

        self.is_deleted = True
        return self.save()

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            raise e


class BaseModel(CRUDMixin, db.Model):
    """Abstract base model with common fields (id, timestamps, is_deleted) and CRUD methods."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now
    )
