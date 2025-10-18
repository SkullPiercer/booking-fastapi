from fastapi import APIRouter, Query, Body, status
from fastapi.responses import JSONResponse

from api.schemas.utils import PaginationDep


router = APIRouter()

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'Сочи'},
    {'id': 2, 'title': 'Дубай', 'name': 'Дубаи'},
    {'id': 3, 'title': 'Istanbul', 'name': 'Стамбул'},
    {'id': 4, 'title': 'Paris', 'name': 'Париж'},
    {'id': 5, 'title': 'Rome', 'name': 'Рим'},
    {'id': 6, 'title': 'London', 'name': 'Лондон'},
    {'id': 7, 'title': 'Tokyo', 'name': 'Токио'},
]


@router.get('/')
def get_hotels(
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля'),
        *,
        pagination: PaginationDep
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    start = (pagination.page - 1) * pagination.per_page
    return hotels_[start: start + pagination.per_page]


@router.post('/')
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title
    })
    return {'status': 'OK'}


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.put('/{hotel_id}')
def update_hotel(
    hotel_id: int,
    title: str = Body(..., description='Название отеля'),
    name: str = Body(..., description='Уникальный идентификатор')
):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)

    if not hotel:
        return JSONResponse(
            content='Отель с таким id не был найден',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    hotel['title'] = title
    hotel['name'] = name
    return hotel
    
    

@router.patch('/{hotel_id}')
def partically_update_hotel(
    hotel_id: int,
    title: str | None = Body(None, description='Название отеля'),
    name: str | None = Body(None, description='Уникальный идентификатор')
):
    hotel = next((h for h in hotels if h['id'] == hotel_id), None)

    if not hotel:
        return JSONResponse(
            content='Отель с таким id не был найден',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    if title:
        hotel['title'] = title
    
    if name:
        hotel['name'] = name
    
    return hotel
