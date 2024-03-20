from fastapi import FastAPI
from starlette.datastructures import QueryParams
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request, HTTPConnection
from starlette.responses import Response
from starlette.types import Scope, Receive, Send, ASGIApp
from core.config import config
from core.fastapi.adapters import BaseAdapter


class env:
    ...


class CompanyMidlleWare:
    def __init__(self, app: ASGIApp, *args, **kwargs):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        conn = HTTPConnection(scope)
        e = env()
        for i, v in config.services.items():
            e.__setattr__(i, BaseAdapter(conn, i))
        scope['env'] = e
        await self.app(scope, receive, send)

