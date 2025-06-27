from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from app.core.db.mixins import TableNameMixin, TimestampMixin

# Base class for ORM models
class Base(AsyncAttrs, DeclarativeBase):
    pass


class Material(Base, TimestampMixin):
    __tablename__ = 'materials'  # Explicitly set the table name
    name_material: Mapped[str] = Column(String, nullable=False)
    time_material: Mapped[float] = Column(Float, nullable=False)
    note_material: Mapped[str] = Column(String, nullable=True)


