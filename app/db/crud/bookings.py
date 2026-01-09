from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select

from app.api.exceptions.timed_base import AllRoomsAreBookedException
from app.api.schemas.bookings import BookingCreateSchema
from app.db.crud.base import CRUDBase
from app.db.crud.mappers.bookings import BookingsMapper
from app.db.crud.utils import get_ids_for_booking
from app.db.models import Bookings


class CRUDBookings(CRUDBase):
    model = Bookings
    mapper = BookingsMapper

    async def get_bookings_with_today_checkin(self):
        query = select(Bookings).filter(Bookings.date_from == date.today())
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking)
            for booking in res.scalars().all()
        ]

    async def add_booking(self, data: BookingCreateSchema, hotel_id: int):
        rooms_ids_to_get = get_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.create(data)
            return new_booking

        raise AllRoomsAreBookedException
