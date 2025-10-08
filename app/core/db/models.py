from sqlalchemy import Column, Float, Date, Integer, String
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


    class User(Base):
        __tablename__ = "users"

        username: Mapped[str] = Column(String(50), unique=True, nullable=False)
        password_hash: Mapped[str] = Column(String(128), nullable=False)
        role: Mapped[str] = Column(String(20), nullable=False, default="user")  # "admin" or "user"

        def __repr__(self):
            return f"<User(username={self.username}, role={self.role})>"
