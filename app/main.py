from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from contextlib import asynccontextmanager
from rich import print, table
from app.core.db import db



os.makedirs("static", exist_ok=True)

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db.engine.begin() as conn:
    #     # Create tables if they do not exist
    #     await conn.run_sync(lambda conn: None)
    
    yield
    # Shutdown logic here
    # await db.engine.dispose()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html" )


