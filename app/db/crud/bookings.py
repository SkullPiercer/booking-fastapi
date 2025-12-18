from app.db.crud.base import CRUDBase
from app.db.crud.mappers.bookings import BookingsMapper
from app.db.models import Bookings


class CRUDBookings(CRUDBase):
    model = Bookings
    mapper = BookingsMapper
