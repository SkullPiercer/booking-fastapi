from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.users import UserCreateSchema
from app.core.db import get_async_session
from app.db.crud.users import CRUDUser


router = APIRouter()

@router.post('/')
async def create_user(
    user: UserCreateSchema,
    session:AsyncSession = Depends(get_async_session)
):
    new_user = await CRUDUser(session).create(user)
    await session.commit()
    return new_user
