from datetime import date

from fastapi import APIRouter, Body, HTTPException, status, Path, Query

from app.api.schemas.facilities import RoomFacilityCreateSchema
from app.api.schemas.rooms import (
    RoomsCreateSchema,
    RoomsPutSchema,
    RoomsPatchSchema,
    RoomsRequestSchema,
    RoomsPatchRequest,
)
from app.api.schemas.utils import PaginationDep
from app.api.examples.rooms import room_examples
from app.api.dep.db import DBDep


router = APIRouter()


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int = Path(..., gt=0),
    date_from: date = Query(...),
    date_to: date = Query(...),
    *,
    pagination: PaginationDep,
    db: DBDep,
):
    result = await db.rooms.get_filtered_by_date(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Отель не найден!"
        )
    return result


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
    db: DBDep,
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
):
    room = await db.rooms.get_one_or_none_with_facilities(
        id=room_id, hotel_id=hotel_id
    )
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комнаты с таким id не существует!",
        )
    return room


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int = Path(..., gt=0),
    new_room: RoomsRequestSchema = Body(..., openapi_examples=room_examples),
):
    try:
        _new_room = RoomsCreateSchema(
            hotel_id=hotel_id, **new_room.model_dump()
        )
        room_db = await db.rooms.create(_new_room)

        if new_room.facilities_ids:
            # TODO: Добавить проверку на существование удобства
            rooms_facilities = [
                RoomFacilityCreateSchema(room_id=room_db.id, facility_id=f_id)
                for f_id in new_room.facilities_ids
            ]
            await db.rooms_facilities.create_bulk(rooms_facilities)

        await db.commit()
        return room_db
    except Exception as e:
        print(e)
        # TODO: Разделить проверку на существование отеля и дубля title
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/{hotel_id}/rooms/bulk")
async def create_rooms(
    db: DBDep,
    hotel_id: int = Path(..., gt=0),
    *,
    new_rooms: list[RoomsRequestSchema],
):
    try:
        _new_rooms = [
            RoomsCreateSchema(hotel_id=hotel_id, **room.model_dump())
            for room in new_rooms
        ]
        new_rooms_db = await db.rooms.create_bulk(_new_rooms)

        rooms_facilities = [
            RoomFacilityCreateSchema(room_id=room.id, facility_id=facility_id)
            for room, input_room in zip(new_rooms_db, new_rooms)
            for facility_id in (input_room.facilities_ids or [])
        ]

        if rooms_facilities:
            await db.rooms_facilities.create_bulk(rooms_facilities)

        await db.commit()
        return new_rooms_db

    except Exception as e:
        print(e)
        # TODO: Разделить проверку на существование отеля и дубля title
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep, hotel_id: int = Path(..., gt=0), room_id: int = Path(..., gt=0)
):
    deleted_room = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return deleted_room


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_update_room(
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
    *,
    new_room_data: RoomsPatchRequest,
    db: DBDep,
):
    # TODO: Добавить проверку на то что отель существует
    _new_room_data = RoomsPatchSchema(
        hotel_id=hotel_id, **new_room_data.model_dump(exclude_unset=True)
    )
    updated_room = await db.rooms.update(
        new_data=_new_room_data, partially=True, id=room_id, hotel_id=hotel_id
    )

    if new_room_data.facilities_ids is not None:
        await db.rooms_facilities.update(
            room_id=updated_room.id, new_data=new_room_data.facilities_ids
        )

    await db.commit()
    return updated_room


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
    *,
    new_room_data: RoomsRequestSchema,
    db: DBDep,
):
    _new_room_data = RoomsPutSchema(
        hotel_id=hotel_id, **new_room_data.model_dump()
    )
    updated_room = await db.rooms.update(new_data=_new_room_data, id=room_id)
    await db.rooms_facilities.update(
        room_id=updated_room.id, new_data=new_room_data.facilities_ids
    )
    await db.commit()
    return updated_room
