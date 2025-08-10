import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.work_time.models import WorkTime
from app.api.work_time.schema import WorkTimeCreate

from sqlalchemy import select


class WorkTimeService:
    @classmethod
    async def create_work_time(
        cls, work_time_data: WorkTimeCreate, session: AsyncSession
    ) -> WorkTime:
        work_time_dict = work_time_data.model_dump()

        db_work_time = WorkTime(**work_time_dict)

        session.add(db_work_time)
        await session.commit()

        return db_work_time

    @classmethod
    async def get_work_time_by_id(cls, work_time_id: uuid.UUID, session: AsyncSession):
        work_time = await session.get(WorkTime, work_time_id)
        if not work_time:
            raise ValueError(f"WorkTime with id {work_time_id} not found")
        return work_time

    @classmethod
    async def update_work_time(
        cls,
        work_time_id: uuid.UUID,
        work_time_data: WorkTimeCreate,
        session: AsyncSession,
    ):
        work_time = await session.get(WorkTime, work_time_id)
        if not work_time:
            raise ValueError(f"WorkTime with id {work_time_id} not found")

        for key, value in work_time_data.model_dump().items():
            setattr(work_time, key, value)

        session.add(work_time)
        await session.commit()
        return work_time

    @classmethod
    async def delete_work_time(cls, work_time_id: uuid.UUID, session: AsyncSession):
        work_time = await session.get(WorkTime, work_time_id)
        if not work_time:
            raise ValueError(f"WorkTime with id {work_time_id} not found")

        await session.delete(work_time)
        await session.commit()
        return work_time

    @classmethod
    async def list_work_times(cls, session: AsyncSession):
        result = await session.execute(select(WorkTime))
        return result.scalars().all()
