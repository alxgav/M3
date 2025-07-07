import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import engine
from sqlalchemy import text
from fastapi.responses import HTMLResponse, JSONResponse

os.makedirs("static", exist_ok=True)

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html" )

# todo
# @app.get("/", response_class=HTMLResponse)
# def index(request: Request):
#     stations = services.get_stations()
#     final_response = services.get_final_data()
#     data = {
#         "stations": stations,
#         "final_response": final_response}
#     return templates.TemplateResponse(name='index.html', request=request, context={"request": request, "data": data})

@app.get("/test-db-connection")
async def test_db_connection():
    try:
        async with AsyncSession(engine) as session:
            # Execute a simple SQL query to test the connection
            result = await session.execute(text("SELECT 1"))
            if result.scalar() == 1:
                return JSONResponse(
                    content={"status": "success", "message": "Database connection successful"}
                )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
