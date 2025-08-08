import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.api.routers.routers import router
from app.services.services import get_final_data
from app.core.db.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router, prefix="")



