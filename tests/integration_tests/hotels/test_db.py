from app.api.schemas.hotels import HotelCreateSchema


async def test_create_hotel(db):
    hotel_data = HotelCreateSchema(
        title='Тестовый отель',
        location='Планета земля'
    )
    new_hotel = await db.hotels.create(hotel_data)
    await db.commit()
    print(f'{new_hotel=}')
