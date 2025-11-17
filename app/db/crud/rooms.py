from app.api.schemas.rooms import RoomsDBSchema
from app.db.crud.base import CRUDBase
from app.db.models.rooms import Rooms

class CRUDRooms(CRUDBase):
    model = Rooms
    schema = RoomsDBSchema

