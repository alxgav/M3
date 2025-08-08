import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from app.api.routers.routers import router
from app.services.services import get_final_data
from app.core.db.db import engine



# from app.api.routes import routers





@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router, prefix="")

# @app.get("/", response_class=HTMLResponse)
# async def final_data(request: Request):
#    final_data = get_final_data()

#    # print(final_data)
#    return templates.TemplateResponse(
#        request=request, name="index.html", context={"final_data": final_data}
#    )


