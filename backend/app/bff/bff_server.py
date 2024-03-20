from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Scope, Receive, Send

from app.bff.bff_config import config
from app.bff.bff_router import bff_router
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBffBackend,
    SQLAlchemyMiddleware,
)
from core.helpers.cache import Cache, CustomKeyMaker
from core.helpers.cache import RedisBackend


class env:
    ...


class AdapterMidlleWare:
    """
    Адартер кладется в request для удобства
    """

    def __init__(self, app: ASGIApp, *args, **kwargs):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        conn = HTTPConnection(scope)
        e = env()
        for i, v in config.services.items():
            e.__setattr__(i, v['adapter'](conn, i))
        scope['env'] = e
        await self.app(scope, receive, send)


def init_routers(app_: FastAPI) -> None:
    app_.include_router(bff_router)


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(AdapterMidlleWare),
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBffBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),

    ]
    return middleware


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()
    return app_


app = create_app()

app.mount("/static", StaticFiles(directory="app/bff/static"), name="static")
# app.mount("/static", StaticFiles(directory="app/bff/static"), name="static")
# app.add_middleware(GZipMiddleware)
