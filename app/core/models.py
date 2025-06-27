from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from app.core.db.mixins import TableNameMixin, TimestampMixin

# Base class for ORM models
class Base(AsyncAttrs, DeclarativeBase):
    pass


class Material(Base, TimestampMixin):
    __tablename__ = 'materials'  
    name_material: Mapped[str] = Column(String, nullable=False)
    time_material: Mapped[float] = Column(Float, nullable=False)
    note_material: Mapped[str] = Column(String, nullable=True)

class Workout(Base, TimestampMixin):
    __tablename__ = 'workouts'  
    shift_work: Mapped[str] = Column(String, nullable=False)
    time_workout: Mapped[float] = Column(Float, nullable=False)
    user_id: Mapped[str] = mapped_column(String, nullable=False)

class WorkoutMaterial(Base, TimestampMixin):
    __tablename__ = 'workout_materials'  
    workout_id: Mapped[str] = mapped_column(String, nullable=False)
    material_id: Mapped[str] = mapped_column(String, nullable=False)
    time_workout_material: Mapped[float] = Column(Float, nullable=False)
    note_workout_material: Mapped[str] = Column(String, nullable=True)

class User(Base, TimestampMixin):
    __tablename__ = 'users'  
    username: Mapped[str] = Column(String, unique=True, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)
    is_active: Mapped[bool] = Column(String, default=True, nullable=False)