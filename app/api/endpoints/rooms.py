import sqlalchemy
from fastapi import APIRouter, Body, HTTPException, status, Path

from app.api.schemas.rooms import (
    RoomsCreateSchema,
    RoomsPutSchema,
    RoomsPatchSchema,
    RoomsRequestSchema,
    RoomsPatchRequest
)
from app.api.schemas.utils import PaginationDep
from app.api.examples.rooms import room_examples
from app.api.dep.db import DBDep

router = APIRouter()

@router.get('/{hotel_id}/rooms')
async def get_all_rooms(
    hotel_id: int = Path(..., gt=0),
    *,
    pagination: PaginationDep,
    db: DBDep
):
    result = await db.rooms.get_list(hotel_id=hotel_id)
    if not result:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Отель не найден!'
            )   
    return result
    


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room_by_id(
    db: DBDep,
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
):
    room = await db.rooms.get_one_or_none(
        id=room_id, hotel_id=hotel_id
    )
    if room is  None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Комнаты с таким id не существует!'
            )   
    return room


@router.post('/{hotel_id}/rooms')
async def create_room(
    db: DBDep,
    hotel_id: int = Path(..., gt=0),
    new_room: RoomsRequestSchema = Body(..., openapi_examples=room_examples)
):
    try:
        _new_room = RoomsCreateSchema(hotel_id=hotel_id, **new_room.model_dump())
        room_db = await db.rooms.create(_new_room)
        await db.commit()
        return room_db
    
    except sqlalchemy.exc.IntegrityError as e:
        # TODO: Добавить отдельный exc на дубль по title
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Отеля с таким id не существует!'
        )



@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
    db: DBDep,
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0)
):
    deleted_room = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return deleted_room


@router.patch('/{hotel_id}/rooms/{room_id}')
async def partially_update_room(
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
    *,
    new_room_data: RoomsPatchRequest,
    db: DBDep
):
    # TODO: Добавить проверку на то что отель существует
    _new_room_data = RoomsPatchSchema(
        hotel_id=hotel_id,
        **new_room_data.model_dump(exclude_unset=True)
    )
    updated_room = await db.rooms.update(
        new_data=_new_room_data, partially=True, id=room_id, hotel_id=hotel_id
    )
    await db.commit()
    return updated_room


@router.put('/{hotel_id}/rooms/{room_id}')
async def update_room(
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
    *,
    new_room_data: RoomsRequestSchema,
    db: DBDep
):
    _new_room_data = RoomsPutSchema(hotel_id=hotel_id, **new_room_data.model_dump())
    updated_room = await db.rooms.update(
        new_data=_new_room_data, id=room_id
    )
    await db.commit()
    return updated_room
