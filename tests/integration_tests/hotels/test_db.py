from app.api.dep.db import DBManager
from app.api.schemas.hotels import HotelCreateSchema
from app.core.db import async_session_maker


async def test_create_hotel():
    hotel_data = HotelCreateSchema(
        title='Тестовый отель',
        location='Планета земля'
    )

    async with DBManager(session_factory=async_session_maker) as db:
        new_hotel = await db.hotels.create(hotel_data)
        await db.commit()
        print(f'{new_hotel=}')
