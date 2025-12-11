from fastapi import APIRouter

from app.api.endpoints import bookings_router, hotels_router, users_router, rooms_router

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(
    users_router,
    prefix='/users',
    tags=('Пользовательская зона',)
)

main_router.include_router(
    hotels_router,
    prefix='/hotels',
    tags=('Отели',)
)

main_router.include_router(
    rooms_router,
    prefix='/hotels',
    tags=('Комнаты',)
)

main_router.include_router(
    bookings_router,
    prefix=('/bookings'),
    tags=('Бронирование',)
)
