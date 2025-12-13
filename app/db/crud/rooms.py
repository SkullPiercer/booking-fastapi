from app.api.schemas.rooms import RoomsDBSchema
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
        result = get_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_list(Rooms.id.in_(result))
