from app.api.schemas.rooms import RoomsDBSchema
from app.db.crud.mappers.base import DataMapper
from app.db.models import Rooms


class RoomsMapper(DataMapper):
    model = Rooms
    schema = RoomsDBSchema
