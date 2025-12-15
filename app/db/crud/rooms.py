from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.schemas.rooms import RoomsDBSchema, RoomWithRels
from app.db.crud.base import CRUDBase
from app.db.crud.utils import get_ids_for_booking
from app.db.models import Rooms

class CRUDRooms(CRUDBase):
    model = Rooms
    schema = RoomsDBSchema

    async def get_filtered_by_date(
        self,
        hotel_id,
        date_from,
        date_to
    ):
        available_rooms = get_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(available_rooms))
        )
        result = await self.session.execute(query)
        return [
                RoomWithRels.model_validate(obj, from_attributes=True)
                for obj in result.scalars().all()
            ]

    async def get_one_or_none_with_facilities(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
