from typing import Annotated, Optional, Any

from fastapi import APIRouter, Depends
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator, UUID4, model_validator
from starlette.datastructures import QueryParams
from starlette.responses import Response, JSONResponse

from app.bff.bff_service import BffService
from app.bff.dff_helpers.filters_cleaner import clean_filter
from app.bff.dff_helpers.schema_recognizer import ModelView
from app.bff.template_spec import templates


class ExceptionResponseSchema(BaseModel):
    error: str


index_router = APIRouter(
    responses={"400": {"model": ExceptionResponseSchema}},
)


@index_router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse(request, 'index-full.html', context={})


@index_router.get("/htmx/footer", response_class=HTMLResponse)
async def footer(request: Request):
    return templates.TemplateResponse(request, 'partials/footer.html', context={})


@index_router.get("/htmx/topbar", response_class=HTMLResponse)
async def topbar(request: Request):
    return templates.TemplateResponse(request, 'partials/topbar.html', context={})


@index_router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse(request, 'index.html', context={})


@index_router.get("/auth/login",responses={"404": {"model": ExceptionResponseSchema}},)
async def login(request: Request, response: Response):
    return templates.TemplateResponse(request, 'auth/login-full.html', context={})


@index_router.post(
    "/auth/login",
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def login(
        request: Request,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()]):

    async with request.scope['env'].basic as a:
        data = await a.login(username, password)
    return templates.TemplateResponse(request, 'components/write_ls.html', context={'token': data['token'], 'refresh_token': data['refresh_token']})


class RefreshTokenSchema(BaseModel):
    token: str
    refresh_token: str


@index_router.post("/basic/user/refresh", responses={"404": {"model": ExceptionResponseSchema}}, )
async def refresh_token(request: Request, refresh_schema: RefreshTokenSchema):
    async with request.scope['env'].basic as a:
        return await a.refresh_token(refresh_schema)


class SelectSchema(BaseModel):
    module: str
    model: str
    prefix: str
    name: str
    value: str = None
    required: bool = False
    title: str = None
    search_terms: Any = None

    @field_validator('value')
    @classmethod
    def check_none(cls, v: Any):
        if v == 'None':
            return None
        return v

    @field_validator('required', 'value')
    @classmethod
    def check_none(cls, v: Any):
        if v == 'None':
            return None
        return v



class FilterSchema(BaseModel):
    module: str
    model: str
    prefix: str


@index_router.post("/bff/filter", response_class=HTMLResponse)
async def filter(request: Request, filschema: FilterSchema):
    """
     Универсальный запрос, который отдает фильтр обьекта по его модулю и модели
    """
    htmx_orm = ModelView(request, filschema.module, filschema.model, prefix=filschema.prefix)
    return htmx_orm.get_filter()


class MultiSelectSchema(BaseModel):
    module: str
    model: str
    prefix: str
    field_name: str
    select_in: str | None
    values: list[UUID4] = []
    search_terms: str

    @classmethod
    def parse_values(cls, v: str):
        try:
            return list(set(eval(v)))
        except Exception as ex:
            pass
    @model_validator(mode='before')
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict):
            prefix = data['prefix']
            field_name = data['field_name']
            values = cls.parse_values(data['values'])
            select_in = data.get('select_in')
            if select_in:
                values = data[f'{prefix}{field_name}']
            data['select_in'] = select_in
            data['values'] = values
            data['search_terms'] = max(data['search_terms']) if data.get('search_terms') else ''
        return data

class SearchSchema(BaseModel):
    module: str
    model: str
    query: str = ''
@index_router.get("/bff/search", response_class=JSONResponse)
async def search(request: Request, schema:SearchSchema = Depends(SearchSchema)):
    """
     Универсальный запрос поиска
    """
    params = QueryParams({'search': schema.query})
    async with getattr(request.scope['env'], schema.module) as a:
        data = await a.list(params=params, model=schema.model)
    return [
        {
            'value': i['id'],
            'label': i.get('title') or i.get('name') or i.get('english_name')
        }
        for i in data['data']
    ]

class SearchIds(BaseModel):
    module: str
    model: str
    id__in: str
@index_router.get("/bff/get_by_ids", response_class=JSONResponse)
async def get_by_ids(request: Request, schema: SearchSchema = Depends(SearchIds)):
    """
     Универсальный запрос поиска
    """
    if not schema.id__in:
        return []
    params = QueryParams({'id__in': schema.id__in})
    async with getattr(request.scope['env'], schema.module) as a:
        data = await a.list(params=params, model=schema.model)
    return [
        {
            'value': i['id'],
            'label': i.get('title') or i.get('name') or i.get('english_name')
        }
        for i in data['data']
    ]


class BadgesSchema(BaseModel):
    model: str
    module: str
    value: str | dict = None
    prefix: str

    @field_validator('value')
    @classmethod
    def check_none(cls, v: Any):
        if v:
            try:
                return eval(v)
            except Exception as ex:
                pass
        return None




class TableSchema(BaseModel):
    module: str
    model: str
    cursor: Optional[int] = 0
    prefix: str


@index_router.post("/base/table", response_class=HTMLResponse)
async def table(request: Request, schema: TableSchema):
    """
     Универсальный запрос, который отдает таблицу обьекта и связанные если нужно
    """
    form_data = await request.json()
    qp = request.query_params
    if form_data.get('prefix'):
        data = clean_filter(form_data, form_data['prefix'])
        qp = {i: v for i, v in data.items() if v}
    view = ModelView(request, params=qp, module=schema.module, model=schema.model, prefix=schema.prefix)
    return await view.get_table()


class ModalSchema(BaseModel):
    prefix: str
    module: str
    model: str
    method: str
    id: Optional[UUID4] = None
    target_id: str = None

    class Config:
        extra = 'allow'

@index_router.post("/base/modal", response_class=HTMLResponse)
async def modal(request: Request, schema: ModalSchema):
    """
     Универсальный запрос, который отдает форму модели (черпает из ModelUpdateSchema
    """
    model = ModelView(request, schema.module, schema.model, prefix=schema.prefix)
    if data := schema.model_extra:
        data = clean_filter(data, schema.prefix)
        method_schema = getattr(model.schemas, schema.method)
        method_schema_obj = method_schema(**data)
        adapter_method = getattr(model.adapter, schema.method)
        responce = await adapter_method(id=schema.id, model=schema.model, json=method_schema_obj.model_dump(mode='json'))
        return model.send_message(f'{model.model.capitalize()}: is {schema.method.capitalize()}')
    else:
        model_method = getattr(model, f'get_{schema.method}')
        return await model_method(model_id=schema.id, target_id=schema.target_id)


@index_router.get("/base/dropdown-ids", response_class=HTMLResponse)
async def dropdown_ids(request: Request, module: str, model: str, id: str, itemlink: str, is_named=False) -> dict:
    """
     Виджет на вход получает модуль-модель-ид- и обратную ссылку если нужно, если нет будет /module/model/{id}
     _named означает, что так же будет отдат name для отрисовки на тайтле кнопки
    """
    data = await BffService.dropdown_ids(request, module, model, id, itemlink, is_named)
    return templates.TemplateResponse(request, 'widgets/widgets/dropdown-ids-named-htmx.html', context=data)
