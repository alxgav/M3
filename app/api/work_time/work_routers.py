import uuid

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.work_time.schema import WorkTime, WorkTimeCreate
from app.api.work_time.services import WorkTimeService
from app.core.db.db import get_db

work_time_router = APIRouter()


@work_time_router.post(
    "/work_times", status_code=status.HTTP_201_CREATED, response_model=WorkTime
)
async def create_work_time(
    work_time_data: WorkTimeCreate, session: AsyncSession = Depends(get_db)
) -> WorkTime:
    work_time = await WorkTimeService.create_work_time(work_time_data, session)
    return work_time


@work_time_router.get(
    "/work_times/{work_time_id}",
    response_model=WorkTime,
    status_code=status.HTTP_200_OK,
)
async def get_work_time(
    work_time_id: uuid.UUID, session: AsyncSession = Depends(get_db)
) -> WorkTime:
    work_time = await WorkTimeService.get_work_time_by_id(work_time_id, session)
    return work_time


@work_time_router.get(
    "/work_times", response_model=list[WorkTime], status_code=status.HTTP_200_OK
)
async def list_work_times(session: AsyncSession = Depends(get_db)) -> list[WorkTime]:
    work_times = await WorkTimeService.list_work_times(session)
    return work_times


@work_time_router.put(
    "/work_times/{work_time_id}",
    response_model=WorkTime,
    status_code=status.HTTP_200_OK,
)
async def update_work_time(
    work_time_id: uuid.UUID,
    work_time_data: WorkTimeCreate,
    session: AsyncSession = Depends(get_db),
) -> WorkTime:
    updated_work_time = await WorkTimeService.update_work_time(
        work_time_id, work_time_data, session
    )
    return updated_work_time


@work_time_router.delete(
    "/work_times/{work_time_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_work_time(
    work_time_id: uuid.UUID, session: AsyncSession = Depends(get_db)
):
    await WorkTimeService.delete_work_time(work_time_id, session)
    return {"message": f"id {work_time_id} deleted successfully"}
