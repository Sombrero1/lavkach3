import asyncio
import base64
from typing import Annotated
from fastapi import Form
import aiohttp
import jwt
from babel.core import LOCALE_ALIASES
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Response, Request
from starlette.responses import Response
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi_htmx import htmx_init, htmx, TemplateSpec as ts

from app.bff.template_spec import templates
from app.bff.dff_helpers.htmx_decorator import s

htmx_init(templates, file_extension='html')


class ExceptionResponseSchema(BaseModel):
    error: str


index_router = APIRouter(
    responses={"400": {"model": ExceptionResponseSchema}},
)


@index_router.get("/", response_class=HTMLResponse)
@htmx(*s('index'))
async def root_page(request: Request):
    return {"greeting": "Hello World"}


@index_router.get("/htmx/footer", response_class=HTMLResponse)
@htmx(*s('partials/footer'))
async def footer(request: Request):
    await asyncio.sleep(5)
    return {"greeting": "Hello World"}


@index_router.get("/htmx/topbar", response_class=HTMLResponse)
@htmx(*s('partials/topbar'))
async def topbar(request: Request):
    return {"greeting": "Hello World"}


@index_router.get("/", response_class=HTMLResponse)
@htmx(*s('index'))
async def root_page(request: Request):
    return {"greeting": "Hello World"}


@index_router.get(
    "/auth/login",
    responses={"404": {"model": ExceptionResponseSchema}},
)
@htmx(*s('auth/login'))
async def login(request: Request, response: Response):
    return {}


@index_router.post(
    "/auth/login",
    responses={"404": {"model": ExceptionResponseSchema}},
)
@htmx(*s('helpers/write_ls'))
async def login(
        request: Request,
        response: Response,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()]):
    async with aiohttp.ClientSession() as session:
        body = {
            'email': username,
            'password': password
        }
        async with session.post('http://127.0.0.1:8001/api/user/login', json=body) as bresp:
            data = await bresp.json()
    response.set_cookie(key='token', value=data['token'], httponly=True)
    response.set_cookie(key='refresh_token', value=data['refresh_token'], httponly=True)
    return {'token': data['token'], 'refresh_token': data['refresh_token']}
