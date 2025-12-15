from sqlalchemy import select, insert, delete

from app.api.schemas.facilities import FacilityDB, RoomFacilityDB
from app.db.crud.base import CRUDBase
from app.db.models.facilities import Facilities, RoomsFacilities


class CRUDFacility(CRUDBase):
    model = Facilities
    schema = FacilityDB


class CRUDRoomFacility(CRUDBase):
    model = RoomsFacilities
    schema = RoomFacilityDB

    async def update(self, room_id, new_data):
        room_facilities = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(room_facilities)
        current_ids = {id for id in result.scalars().all()}

        _new_data = set(new_data)
        to_add = _new_data - current_ids
        to_delete = current_ids - _new_data

        if to_add:
            query = insert(self.model).values(
                [
                    {'room_id':room_id, 'facility_id':f_id
                    } for f_id in to_add
                ]
            )
            await self.session.execute(query)

        if to_delete:
            query = delete(self.model).where(
                self.model.room_id == room_id,
                self.model.facility_id.in_(to_delete)
            )
            await self.session.execute(query)