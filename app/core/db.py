from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(url=settings.DB_URL)

async def func():
    async with engine.begin() as conn:
        res = await conn.execute(text('SELECT version()'))
        print(res.fetchone())

import asyncio
asyncio.run(func())