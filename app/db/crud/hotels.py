from datetime import date

from sqlalchemy import select, func

from app.api.exceptions.timed_base import DateException
from app.db.crud.base import CRUDBase
from app.db.crud.mappers.hotels import HotelsMapper
from app.db.crud.utils import get_ids_for_booking
from app.db.models import Rooms
from app.db.models.hotels import Hotels


class CRUDHotels(CRUDBase):
    model = Hotels
    mapper = HotelsMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        limit: int,
        offset: int,
        title: str | None = None,
        location: str | None = None,
    ):
        rooms_ids_to_get = get_ids_for_booking(date_from, date_to)
        hotels_ids = (
            select(Rooms.hotel_id)
            .select_from(Rooms)
            .filter(Rooms.id.in_(rooms_ids_to_get))
        )

        query = select(self.model).filter(Hotels.id.in_(hotels_ids))

        if location is not None:
            query = query.filter(
                func.lower(Hotels.location).contains(location.strip().lower())
            )

        if title is not None:
            query = query.filter(
                func.lower(Hotels.title).contains(title.strip().lower())
            )

        query = query.limit(limit).offset(offset)

        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(obj)
            for obj in res.scalars().all()
        ]
