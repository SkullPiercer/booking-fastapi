from app.api.schemas.facilities import FacilityDB, RoomFacilityDB
from app.db.crud.mappers.base import DataMapper
from app.db.models import Facilities, RoomsFacilities


class FacilitiesMapper(DataMapper):
    model = Facilities
    schema = FacilityDB


class RoomFacilitiesMapper(DataMapper):
    model = RoomsFacilities
    schema = RoomFacilityDB
