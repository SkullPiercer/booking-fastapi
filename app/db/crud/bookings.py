from app.api.schemas.bookings import BookingDBSchema
from app.db.crud.base import CRUDBase
from app.db.models import Bookings


class CRUDBookings(CRUDBase):
    model = Bookings
    schema = BookingDBSchema
