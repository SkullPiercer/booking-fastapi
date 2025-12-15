from app.api.schemas.hotels import HotelDBSchema
from app.db.crud.mappers.base import DataMapper
from app.db.models import Hotels


class HotelsMapper(DataMapper):
    model = Hotels
    schema = HotelDBSchema
