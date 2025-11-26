from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.users import UserCreateSchema, UserTokenSchema
from app.api.dep.user import UserIdDep
from app.api.dep.db import DBDep
from app.core.db import get_async_session
from app.core.user import AuthService
from app.db.crud.users import CRUDUser


router = APIRouter()

@router.post('/register')
async def create_user(
    user: UserCreateSchema,
    db: DBDep
):
    new_user = await db.users.create(user)
    await db.commit()
    return new_user

@router.post('/login')
async def create_user_token(
    user: UserTokenSchema,
    response: Response,
    db: DBDep
):
    user_db = await db.users.get_user_with_pass(email=user.email)
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
    
    access_token = AuthService().create_access_token({'user_id': user_db.id})
    response.set_cookie(key='access_token', value=access_token)
    return {'access_token': access_token}


@router.get('/me')
async def get_data_auth_only(
    user_id: UserIdDep,
    db: DBDep
):
    return await db.users.get_one_or_none(id=user_id)


@router.post('/logout')
async def logout(
    response: Response
):
    response.delete_cookie('access_token')
    return 'Вы успешно вышли из системы!'
        