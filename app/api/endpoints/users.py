from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.users import UserCreateSchema, UserTokenSchema
from app.core.db import get_async_session
from app.core.user import AuthService
from app.db.crud.users import CRUDUser


router = APIRouter()

@router.post('/register')
async def create_user(
    user: UserCreateSchema,
    session:AsyncSession = Depends(get_async_session)
):
    new_user = await CRUDUser(session).create(user)
    await session.commit()
    return new_user

@router.post('/login')
async def create_user_token(
    user: UserTokenSchema,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
):
    user_db = await CRUDUser(session).get_user_with_pass(email=user.email)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проверьте правильность email и пароля'
        )

    if not AuthService().verify_password(user.password, user_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проверьте правильность email и пароля'
        )

    access_token = {
        'access_token': AuthService().create_access_token({'user_id': user_db.id})
    }
    response.set_cookie('access_token', access_token)
    return access_token


@router.get('/auth_only')
async def get_data_auth_only(request: Request):
    access_token = request.cookies.get('access_token', None)
    if access_token is not None:
        return 'ok'
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Пожалуйста войдите в систему!'
    )