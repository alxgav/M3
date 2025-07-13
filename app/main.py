import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.services import get_final_data
from rich import print


from app.core.db.db import engine

os.makedirs("static", exist_ok=True)
os.makedirs("app/uploads", exist_ok=True)

templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def final_data(request: Request):
   final_data = get_final_data()

   # print(final_data)
   return templates.TemplateResponse(
       request=request, name="index.html", context={"final_data": final_data}
   )


