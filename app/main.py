import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.backends.inmemory import InMemoryBackend

from app.api.routers import main_router
from app.conectors.redis_connector import redis_manager
from app.core.config import get_settings


logging.basicConfig(level=logging.INFO)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При использовании FastAPI cache, connect можно убрать
    await redis_manager.connect()
    FastAPICache.init(
        RedisBackend(redis_manager.redis), prefix="fastapi-cache"
    )
    logging.info('FastAPI Cache подключен')
    yield
    await redis_manager.disconnect()


# Один из вариантов решить проблему с кешированием в тестах
# if settings.MODE == 'test':
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, port=8002)
