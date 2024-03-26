from functools import wraps
from typing import Any

from .base import BaseBackend, BaseKeyMaker
from .cache_tag import CacheTag
from .custom_key_maker import cache_kay_maker
from .redis_backend import redis_backend


class CacheManager:
    def __init__(self):
        self.backend = redis_backend
        self.key_maker = cache_kay_maker

    def init(self, *, backend: BaseBackend, key_maker: BaseKeyMaker) -> None:
        self.backend = backend
        self.key_maker = key_maker

    def cached(
        self,
        *,
        prefix: str | None = None,
        tag: CacheTag | None = None,
        ttl: int = 60,
    ):
        def _cached(function):
            @wraps(function)
            async def __cached(*args, **kwargs):
                if not self.backend or not self.key_maker:
                    raise Exception("backend or key_maker is None")

                key = await self.key_maker.make(
                    function=function,
                    prefix=prefix if prefix else tag.value,
                )
                cached_response = await self.backend.get(key=key)
                if cached_response:
                    return cached_response

                response = await function(*args, **kwargs)
                await self.backend.set(response=response, key=key, ttl=ttl)
                return response

            return __cached

        return _cached

    async def set(self, *, tag: CacheTag, key: str, response=Any, ttl=None) -> None:
        key = f'{tag.value}::{key}'
        await self.backend.set(response=response, key=key, ttl=ttl)
        return key


    async def remove_by_tag(self, *, tag: CacheTag, key:str=None) -> None:
        key = f'{tag.value}::{key}'
        await self.backend.delete_startswith(key=key)

    async def remove_by_prefix(self, *, prefix: str) -> None:
        await self.backend.delete_startswith(value=prefix)




Cache = CacheManager()
