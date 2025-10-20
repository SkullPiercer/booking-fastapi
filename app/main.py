import uvicorn
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import get_settings

from app.core.db import *

settings = get_settings()

app = FastAPI(title=settings.APP_TITLE)

app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True)
