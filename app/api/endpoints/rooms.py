from fastapi import APIRouter, Body

from app.api.schemas.rooms import RoomCreateSchema
from app.api.examples.rooms import room_examples

router = APIRouter()

@router.get('/')
async def get_all_rooms():
    return ...


@router.get('/{room_id}')
async def get_room_by_id(room_id: int):
    return ...


@router.post('/')
async def create_room(
    new_room: RoomCreateSchema = Body(..., openapi_examples=room_examples)
):
    return new_room


@router.delete('/{room_id}')
async def delete_room(room_id):
    return ...


@router.patch('/{room_id}')
async def partially_update_room(room_id):
    return ...


@router.put('/{room_id}')
async def update_room(room_id):
    return ...