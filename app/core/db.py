from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.DB_URL)
