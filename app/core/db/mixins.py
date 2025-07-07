import re
from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class TableNameMixin:
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, '__tablename__'):
            # Convert CamelCase to snake_case and pluralize by appending 's'
            name = cls.__name__
            s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
            snake = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
            cls.__tablename__ = snake + 's'
