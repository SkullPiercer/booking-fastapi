from fastapi import APIRouter, HTTPException, status
import sqlalchemy

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
    try:
        _new_booking = BookingCreateSchema(user_id=user_id, **new_booking.model_dump())
        await db.bookings.create(_new_booking)
        await db.commit()
        return new_booking
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Комнаты не существует'
        )