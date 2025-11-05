from fastapi import APIRouter, Query, Body, status, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.examples import hotel_examples
from app.api.schemas.utils import PaginationDep
from app.api.schemas.hotels import HotelCreateSchema, HotelPutSchema, HotelPatchSchema
from app.core.db import get_async_session
from app.db.crud.hotels import CRUDHotels

router = APIRouter()


@router.get('/{hotel_id}')
async def get_hotel_by_id(
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
    session: AsyncSession = Depends(get_async_session)
):
    return await CRUDHotels(session).get_by_one_by_filter(id=hotel_id)

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
        ..., openapi_examples=hotel_examples
    ),
    session: AsyncSession = Depends(get_async_session)
):
    hotel_db = await CRUDHotels(session).create(new_hotel)
    await session.commit()
    return hotel_db


@router.delete('/{hotel_id}')
async def delete_hotel(
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
    session: AsyncSession = Depends(get_async_session)
):
    deleted_hotel = await CRUDHotels(session).delete(id=hotel_id)
    await session.commit()
    return deleted_hotel


@router.put('/{hotel_id}')
async def update_hotel(
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
    *,
    hotel_data: HotelPutSchema,
    session: AsyncSession = Depends(get_async_session)
):
    updated_hotel = await CRUDHotels(session).update(new_data=hotel_data, id=hotel_id)
    await session.commit()
    return updated_hotel
    
    

@router.patch('/{hotel_id}')
async def partically_update_hotel(
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
    *,
    hotel_data: HotelPatchSchema,
    session: AsyncSession = Depends(get_async_session)
):
    updated_hotel = await CRUDHotels(session).update(new_data=hotel_data, partially=True, id=hotel_id)
    await session.commit()
    return updated_hotel
