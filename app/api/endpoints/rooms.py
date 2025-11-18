import sqlalchemy
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.rooms import (
    RoomsCreateSchema,
    RoomsPutSchema,
    RoomsPatchSchema,
    RoomsRequestSchema,
    RoomsPatchRequest
)
from app.api.schemas.utils import PaginationDep
from app.api.examples.rooms import room_examples
from app.db.crud.rooms import CRUDRooms
from app.core.db import get_async_session

router = APIRouter()

@router.get('/{hotel_id}/rooms')
async def get_all_rooms(
    hotel_id: int = Path(..., gt=0),
    *,
    pagination: PaginationDep,
    session: AsyncSession = Depends(get_async_session),
):
    result = await CRUDRooms(session).get_list(hotel_id=hotel_id)
    if not result:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Отель не найден!'
            )   
    return result
    


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room_by_id(
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_async_session)
):
    room = await CRUDRooms(session).get_one_or_none(
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
    hotel_id: int = Path(..., gt=0),
    new_room: RoomsRequestSchema = Body(..., openapi_examples=room_examples),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        _new_room = RoomsCreateSchema(hotel_id=hotel_id, **new_room.model_dump())
        room_db = await CRUDRooms(session).create(_new_room)
        await session.commit()
        return room_db
    
    except sqlalchemy.exc.IntegrityError as e:
        # TODO: Добавить отдельный exc на дубль по title
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Отеля с таким id не существует!'
        )



@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_async_session)
):
    deleted_room = await CRUDRooms(session).delete(id=room_id, hotel_id=hotel_id)
    await session.commit()
    return deleted_room


@router.patch('/{hotel_id}/rooms/{room_id}')
async def partially_update_room(
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_async_session),
    *,
    new_room_data: RoomsPatchRequest
):
    # TODO: Добавить проверку на то что отель существует
    _new_room_data = RoomsPatchSchema(
        hotel_id=hotel_id,
        **new_room_data.model_dump(exclude_unset=True)
    )
    updated_room = await CRUDRooms(session).update(
        new_data=_new_room_data, partially=True, id=room_id, hotel_id=hotel_id
    )
    await session.commit()
    return updated_room


@router.put('/{hotel_id}/rooms/{room_id}')
async def update_room(
    hotel_id: int = Path(..., gt=0),
    room_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_async_session),
    *,
    new_room_data: RoomsRequestSchema
):
    _new_room_data = RoomsPutSchema(hotel_id=hotel_id, **new_room_data.model_dump())
    updated_room = await CRUDRooms(session).update(
        new_data=_new_room_data, id=room_id
    )
    await session.commit()
    return updated_room
