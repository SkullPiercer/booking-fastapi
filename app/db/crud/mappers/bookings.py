from app.api.schemas.bookings import BookingDBSchema
from app.db.crud.mappers.base import DataMapper
from app.db.models import Bookings


class BookingsMapper(DataMapper):
    model = Bookings
    schema = BookingDBSchema
