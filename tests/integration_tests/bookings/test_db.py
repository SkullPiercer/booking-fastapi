from datetime import date

from app.api.schemas.bookings import BookingCreateSchema, BookingUpdateSchema


async def test_booking_CRUD(db, user, room):
    booking_data = BookingCreateSchema(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2021, month=1, day=1),
        date_to=date(year=2022, month=1, day=15),
        price=100,
    )
    new_booking = await db.bookings.create(booking_data)
    new_booking_from_db = await db.bookings.get_one_or_none(id=new_booking.id)
    assert new_booking_from_db is not None

    updated_booking = await db.bookings.update(
        new_data=BookingUpdateSchema(
            date_from=date(year=2020, month=1, day=1)
        ),
        partially=True,
        id=new_booking_from_db.id,
    )
    assert updated_booking is not None
    assert new_booking_from_db.id == updated_booking.id
    assert updated_booking.date_from == date(year=2020, month=1, day=1)

    await db.bookings.delete(id=new_booking_from_db.id)
    deleted_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert deleted_booking is None
