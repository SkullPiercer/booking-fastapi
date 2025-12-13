from datetime import date

from sqlalchemy import select, func

from app.db.models import Bookings, Rooms

def get_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    rooms_count = (
        select(Bookings.room_id, func.count('*').label('rooms_booked'))
        .select_from(Bookings)
        .filter(Bookings.date_to >= date_from, Bookings.date_from <= date_to)
        .group_by(Bookings.room_id)
        .cte(name='rooms_count')
    )

    rooms_left = (
        select(
            Rooms.id.label('room_id'),
            (Rooms.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label('rooms_left')
        )
        .select_from(Rooms)
        .outerjoin(rooms_count, rooms_count.c.room_id == Rooms.id)
        .cte(name='rooms_left')

    )

    rooms_ids_for_hotel = (
        select(Rooms.id)
        .select_from(Rooms)
    )

    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)


    result = (
        select(rooms_left.c.room_id)
        .select_from(rooms_left)
        .filter(
            rooms_left.c.rooms_left > 0,
            rooms_left.c.room_id.in_(rooms_ids_for_hotel),
        )
    )

    return result