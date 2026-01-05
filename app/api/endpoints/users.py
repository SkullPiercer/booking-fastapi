from fastapi import APIRouter, HTTPException, status, Response

from app.api.dep.db import DBDep
from app.api.dep.user import UserIdDep
from app.api.schemas.users import UserCreateSchema, UserTokenSchema, UserDBSchema
from app.api.schemas.images import ImageCreateSchema
from app.api.schemas.utils import DownloadFileDep, delete_image
from app.core.user import AuthService


router = APIRouter()

@router.post('/register')
async def create_user(
    user: UserCreateSchema,
    db: DBDep
):
    try:
        new_user = await db.users.create(user)

        await db.commit()
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Ошибка ввода логина или пароля, {e}'
        )


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


@router.get('/me', response_model=UserDBSchema)
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


@router.post('/{user_id}/avatar')
async def set_avatar(
    user_id: UserIdDep,
    db: DBDep,
    file: DownloadFileDep
):
    image = await db.images.create(ImageCreateSchema(file_path=file))
    await db.users.update_avatar(user_id, image.id)
    await db.commit()
    return {'OK': True}

@router.delete('/{user_id}/avatar')
async def delete_avatar(
    user_id: UserIdDep,
    db: DBDep
):
    user = await db.users.get_one_or_none(id=user_id)

    if user.image_id is not None:
        image = await db.images.get_one_or_none(id=user.image_id)
        await delete_image(image.file_path)
        await db.users.update_avatar(user_id)
        await db.images.delete(id=image.id)

        await db.commit()
    return {'OK': True}