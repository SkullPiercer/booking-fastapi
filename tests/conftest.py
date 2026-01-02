import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.core.db import Base, engine_null_pool
from app.core.config import get_settings


@pytest.fixture(scope='session', autouse=True)
async def check_mode():
    assert get_settings().MODE == 'test'


@pytest.fixture(scope='session', autouse=True)
async def async_main(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
async def create_user(async_main):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://127.0.0.1:8002/api/v1"
    ) as ac:
        response = await ac.post(
            url='/users/register',
            json={
                'email': 'sasha@mail.ru',
                'password': 'qweqwerty',
                'confirm_password': 'qweqwerty'
            },
        )
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data['email'] == 'sasha@mail.ru'
        assert response_data['id'] == 1