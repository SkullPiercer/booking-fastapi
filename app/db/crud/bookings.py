from datetime import date

from sqlalchemy import select

from app.db.crud.base import CRUDBase
from app.db.crud.mappers.bookings import BookingsMapper
from app.db.models import Bookings


class CRUDBookings(CRUDBase):
    model = Bookings
    mapper = BookingsMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(Bookings)
            .filter(Bookings.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
