from fastapi import APIRouter, HTTPException, status

from app.api.dep.db import DBDep
from app.api.dep.user import UserIdDep
from app.api.exceptions.timed_base import ObjectNotFoundException, AllRoomsAreBookedException
from app.api.schemas.bookings import BookingCreateSchema, BookingRequestSchema


router = APIRouter()


@router.post("/")
async def create_booking(
    user_id: UserIdDep, new_booking: BookingRequestSchema, db: DBDep
):
    try:
        room = await db.rooms.get_one(id=new_booking.room_id)

    except ObjectNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Номер не найден'
        )

    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комнаты не существует",
        )
    price = room.price
    _new_booking = BookingCreateSchema(
        user_id=user_id, price=price, **new_booking.model_dump()
    )

    try:
        await db.bookings.add_booking(_new_booking, hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ex.detail,
        )

    await db.commit()
    return new_booking


@router.get("/all")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_list()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_list(user_id=user_id)
