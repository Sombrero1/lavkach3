from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.bff.dff_helpers.schema_recognizer import ModelView
from app.bff.template_spec import templates

store_router = APIRouter()


@store_router.get("", response_class=HTMLResponse)
async def store(request: Request):
    model = ModelView(request, 'basic', 'store')
    return templates.TemplateResponse(request,'widgets/list-full.html', context={'model': model})
