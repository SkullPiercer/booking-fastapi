from fastapi import APIRouter, Query, Body, status, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.examples import hotel_examples
from app.api.schemas.utils import PaginationDep
from app.api.schemas.hotels import HotelCreateSchema, HotelPutSchema
from app.core.db import get_async_session
from app.db.crud.hotels import CRUDHotels
from app.db.models.hotels import Hotels


router = APIRouter()


@router.get('/')
async def get_hotels(
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Адрес'),
        session: AsyncSession = Depends(get_async_session),
        *,
        pagination: PaginationDep
):
    return await CRUDHotels(session).get_list(
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=((pagination.page - 1) * pagination.per_page) 
    )


@router.post('/')
async def create_hotel(
    new_hotel: HotelCreateSchema = Body(
        ..., openapi_examples=hotel_examples # type: ignore
    ),
    session: AsyncSession = Depends(get_async_session)
):
    hotel_db = await CRUDHotels(session).create(new_hotel)
    await session.commit()
    return hotel_db


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, session: AsyncSession = Depends(get_async_session)):
    deleted_hotel = await CRUDHotels(session).delete(hotel_id)
    await session.commit()
    return deleted_hotel


@router.put('/{hotel_id}')
async def update_hotel(
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
    *,
    hotel_data: HotelPutSchema,
    session: AsyncSession = Depends(get_async_session)
):
    updated_hotel = await CRUDHotels(session).update_partially(hotel_id, hotel_data)
    await session.commit()
    return updated_hotel
    
    

# @router.patch('/{hotel_id}')
# def partically_update_hotel(
#     hotel_id: int,
#     title: str | None = Body(None, description='Название отеля'),
#     name: str | None = Body(None, description='Уникальный идентификатор')
# ):
#     hotel = next((h for h in hotels if h['id'] == hotel_id), None)

#     if not hotel:
#         return JSONResponse(
#             content='Отель с таким id не был найден',
#             status_code=status.HTTP_404_NOT_FOUND
#         )
    
#     if title:
#         hotel['title'] = title
    
#     if name:
#         hotel['name'] = name
    
#     return hotel
