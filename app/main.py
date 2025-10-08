from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.regal.routers import router
from app.api.work_time.work_routers import work_time_router
from app.core.db.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="../app/static"), name="static")
app.include_router(router, prefix="")
app.include_router(work_time_router, prefix="/work_time", tags=["work_time"])



