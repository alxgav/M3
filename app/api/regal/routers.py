from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.services import get_final_data

router = APIRouter()
templates = Jinja2Templates(directory="../app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_materials(request: Request):
    final_data =  get_final_data()  
    return templates.TemplateResponse(
        "index.html", {"request": request, "final_data": final_data}
    )
