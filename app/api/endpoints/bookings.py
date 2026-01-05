from fastapi import APIRouter, HTTPException, status

from app.api.dep.db import DBDep
from app.api.dep.user import UserIdDep
from app.api.schemas.bookings import BookingCreateSchema, BookingRequestSchema


router = APIRouter()

@router.post('/')
async def create_booking(
    user_id: UserIdDep,
    new_booking: BookingRequestSchema,
    db: DBDep
):
    room = await db.rooms.get_one_or_none(id=new_booking.room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Комната не найдена'
        )

    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    if room is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Комнаты не существует'
    )
    price = room.price
    _new_booking = BookingCreateSchema(
        user_id=user_id,
        price=price,
        **new_booking.model_dump()
    )
    await db.bookings.add_booking(_new_booking, hotel.id)
    await db.commit()
    return new_booking


@router.get('/all')
async def get_all_bookings(
    db: DBDep
):
    return await db.bookings.get_list()


@router.get('/me')
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep
):
    return await db.bookings.get_list(user_id=user_id)