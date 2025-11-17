import sqlalchemy
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.rooms import RoomsCreateSchema, RoomsPutSchema, RoomsPatchSchema
from app.api.schemas.utils import PaginationDep
from app.api.examples.rooms import room_examples
from app.db.crud.rooms import CRUDRooms
from app.core.db import get_async_session

router = APIRouter()

@router.get('/')
async def get_all_rooms(
    pagination: PaginationDep,
    session: AsyncSession = Depends(get_async_session),
):
    return await CRUDRooms(session).get_list()



@router.get('/{room_id}')
async def get_room_by_id(
    room_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    room = await CRUDRooms(session).get_one_or_none(id=room_id)
    if room is  None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Комнаты с таким id не существует!'
            )   
    return room


@router.post('/')
async def create_room(
    new_room: RoomsCreateSchema = Body(..., openapi_examples=room_examples),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        room_db = await CRUDRooms(session).create(new_room)
        await session.commit()
        return room_db
    
    except sqlalchemy.exc.IntegrityError as e:
        # TODO: Добавить отдельный exc на дубль по title
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Отеля с таким id не существует!'
        )



@router.delete('/{room_id}')
async def delete_room(
    room_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_async_session)
):
    deleted_room = await CRUDRooms(session).delete(id=room_id)
    await session.commit()
    return deleted_room


@router.patch('/{room_id}')
async def partially_update_room(
    room_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_async_session),
    *,
    new_room_data: RoomsPatchSchema
):
    # TODO: Добавить проверку на то что отель существует
    updated_room = await CRUDRooms(session).update(
        new_data=new_room_data, partially=True, id=room_id
    )
    await session.commit()
    return updated_room


@router.put('/{room_id}')
async def update_room(
    room_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_async_session),
    *,
    new_room_data: RoomsPutSchema
):
    updated_room = await CRUDRooms(session).update(
        new_data=new_room_data, id=room_id
    )
    await session.commit()
    return updated_room