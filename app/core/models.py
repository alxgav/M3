from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base
from app.core.db.mixins import TimestampMixin


class Material(Base, TimestampMixin):
    __tablename__ = "materials"
    name_material: Mapped[str] = Column(String, nullable=False)
    time_material: Mapped[float] = Column(Float, nullable=False)
    note_material: Mapped[str] = Column(String, nullable=True)




