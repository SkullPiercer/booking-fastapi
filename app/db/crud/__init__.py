from app.db.crud.bookings import CRUDBookings
from app.db.crud.hotels import CRUDHotels
from app.db.crud.rooms import CRUDRooms
from app.db.crud.users import CRUDUser
from app.db.crud.facility import CRUDFacility, CRUDRoomFacility
from app.db.crud.images import CRUDImages


__all__ = [
    'CRUDBookings',
    'CRUDHotels',
    'CRUDRooms',
    'CRUDUser',
    'CRUDFacility',
    'CRUDRoomFacility',
    'CRUDImages',
]
