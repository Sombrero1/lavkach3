from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse

from core.fastapi.frontend.schema_recognizer import ModelView
from app.bff.template_spec import templates

uom_router = APIRouter()


@uom_router.get("", response_class=HTMLResponse)
async def uom(request: Request):
    model = ModelView(request, 'basic', 'uom')
    return templates.TemplateResponse(request,'widgets/list-full.html', context={'model': model})

