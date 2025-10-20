from fastapi import APIRouter

from app.api.endpoints import hotels_router

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(hotels_router, prefix='/hotels')
