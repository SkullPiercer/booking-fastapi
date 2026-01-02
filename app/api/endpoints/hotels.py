from datetime import date

from fastapi import APIRouter, Query, Body, Path
from fastapi_cache.decorator import cache

from app.api.examples import hotel_examples
from app.api.schemas.utils import PaginationDep
from app.api.schemas.hotels import HotelCreateSchema, HotelPutSchema, HotelPatchSchema
from app.api.dep.db import DBDep

router = APIRouter()


@router.get('/{hotel_id}')
async def get_hotel_by_id(
    db: DBDep,
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
):
    return await db.hotels.get_by_one_by_filter(id=hotel_id)


@router.get('/')
@cache(expire=10)
async def get_hotels(
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Адрес'),
        date_from: date = Query(...),
        date_to: date = Query(...),
        *,
        pagination: PaginationDep,
        db: DBDep
):
    print('Иду в бд')
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1),
    )


@router.post('/')
async def create_hotel(
    db: DBDep,
    new_hotel: HotelCreateSchema = Body(
        ..., openapi_examples=hotel_examples
    ),
):
    hotel_db = await db.hotels.create(new_hotel)
    await db.commit()
    return hotel_db


@router.post('/bulk')
async def create_hotels(
    db: DBDep,
    new_hotels: list[HotelCreateSchema],
):
    await db.hotels.create_bulk(new_hotels)
    await db.commit()
    return new_hotels


@router.delete('/{hotel_id}')
async def delete_hotel(
    db: DBDep,
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
):
    # TODO: Не удаляется отель, если с ним связана комната
    deleted_hotel = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return deleted_hotel


@router.put('/{hotel_id}')
async def update_hotel(
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
    *,
    hotel_data: HotelPutSchema,
    db: DBDep
):
    updated_hotel = await db.hotels.update(new_data=hotel_data, id=hotel_id)
    await db.session.commit()
    return updated_hotel
    
    

@router.patch('/{hotel_id}')
async def partically_update_hotel(
    hotel_id: int = Path(..., ge=1, description='ID отеля'),
    *,
    hotel_data: HotelPatchSchema,
    db: DBDep
):
    updated_hotel = await db.hotels.update(new_data=hotel_data, partially=True, id=hotel_id)
    await db.session.commit()
    return updated_hotel
