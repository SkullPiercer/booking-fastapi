import pytest

from app.core.db import Base, engine_null_pool
from app.core.config import get_settings


@pytest.fixture(scope='session', autouse=True)
async def async_main():
    settings = get_settings()
    assert settings.MODE == 'test'

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)