from datetime import date

from app.api.schemas.bookings import BookingCreateSchema

async def test_create_booking(db, user, room):
    booking_data = BookingCreateSchema(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2021, month=1, day=1),
        date_to=date(year=2022, month=1, day=15),
        price=100,
    )
    new_booking = await db.bookings.create(booking_data)
    await db.commit()
    print(f'{new_booking=}')