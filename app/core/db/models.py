from sqlalchemy import Column, Float, Date, Integer
from sqlalchemy.orm import Mapped

from app.core.db.base import Base


class WorkTime(Base):
    __tablename__ = "work_times"

    date: Mapped[Date] = Column(Date, nullable=False)
    time_material: Mapped[float] = Column(Float, default=0.0)
    qty_material: Mapped[int] = Column(Integer, default=0)
    time_plus: Mapped[int] = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<WorkTime(date={self.date} "
