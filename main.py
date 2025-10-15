import uvicorn
from fastapi import FastAPI, Query, Body, status
from fastapi.responses import JSONResponse

app = FastAPI(title='Титульник')

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'Сочи'},
    {'id': 2, 'title': 'Дубай', 'name': 'Дубаи'},
]


@app.get('/hotels')
def get_hotels(
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title
    })
    return {'status': 'OK'}


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@app.put('/hotels/{hotel_id}')
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
    
    

@app.patch('/hotels/{hotel_id}')
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

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
