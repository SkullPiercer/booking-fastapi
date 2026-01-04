from pathlib import Path
from random import randint

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient
from unittest import mock

from tests.constants import ROOT_USER_DATA

# Мокаем фастами кэш (это вариант на случай работы с сервисами у которых нет in-memory бэкенда.)
# Важно оставить мок именно тут, до того как мы импортировали всё остальное
mock.patch(
    'fastapi_cache.decorator.cache',
    lambda *args, **kwargs: lambda f: f
).start()

from app.api.dep.db import DBManager
from app.api.schemas.hotels import HotelCreateSchema
from app.api.schemas.rooms import RoomsCreateSchema
from app.api.schemas.users import UserCreateSchema
from app.main import app
from app.core.db import Base, async_session_maker_null_pool, engine
from app.core.config import get_settings
from tests.utils import read_file


BASE_DIR = Path(__file__).resolve().parent
HOTELS_FIXTURE_PATH = BASE_DIR / "hotels_fixture.json"
ROOMS_FIXTURE_PATH = BASE_DIR / "rooms_fixture.json"
FACILIES_FIXTURE_PATH = BASE_DIR / "facilities_fixture.json"


@pytest.fixture(scope='session', autouse=True)
async def check_mode():
    assert get_settings().MODE == 'test'


@pytest.fixture()
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope='session', autouse=True)
async def async_main(check_mode):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def async_client(async_main):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/api/v1",
    ) as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
async def create_hotels(async_client):
    hotels = await read_file(HOTELS_FIXTURE_PATH)
    await async_client.post(
        url='/hotels/bulk',
        json=hotels
    )


@pytest.fixture(scope='session', autouse=True)
async def create_rooms(
    async_client,
    create_facilities,
    create_hotels
):
    rooms = await read_file(ROOMS_FIXTURE_PATH)
    await async_client.post(
        url=f'hotels/{randint(1, 20)}/rooms/bulk',
        json=rooms
    )


@pytest.fixture(scope='session', autouse=True)
async def create_facilities(async_client):
    facilities = await read_file(FACILIES_FIXTURE_PATH)
    await async_client.post(
        url='/facilities/bulk',
        json=facilities
    )

@pytest.fixture()
async def user(db):
    user = await db.users.create(
        UserCreateSchema(
            email="test_user@mail.ru",
            password='qwerty',
            confirm_password='qwerty'
        )
    )
    await db.commit()
    return user


@pytest.fixture()
async def hotel(db):
    hotel = await db.hotels.create(
        HotelCreateSchema(
            title='Ну крутой отель',
            location='И крутое описание'
        )
    )
    await db.commit()
    return hotel

@pytest.fixture()
async def room(db, hotel):
    room = await db.rooms.create(
        RoomsCreateSchema(
            hotel_id=hotel.id,
            title='Крутая комната',
            description='Не менее крутое описание комнаты',
            price=1000,
            quantity=10
        )
    )
    await db.commit()
    return room


@pytest.fixture(scope='session', autouse=True)
async def root_user(async_client):
    response = await async_client.post(
        url='/users/register',
        json=ROOT_USER_DATA,
    )
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['email'] == 'sasha@mail.ru'
    assert response_data['id'] == 1

    return response_data


@pytest.fixture(scope='session')
async def user_client(async_client, root_user):
    user = await async_client.post(
        url='/users/login',
        json=ROOT_USER_DATA
    )
    assert user.cookies.get('access_token') is not None

    yield user