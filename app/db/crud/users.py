from fastapi import HTTPException, status
from sqlalchemy import insert, select, update

from app.api.schemas.users import UserCreateSchema
from app.core.user import AuthService
from app.db.crud.base import CRUDBase
from app.db.crud.mappers.users import UsersMapper
from app.db.models import Users


class CRUDUser(CRUDBase):
    model = Users
    mapper = UsersMapper

    async def create(self, obj: UserCreateSchema):
        existing_user = await self.get_one_or_none(email=obj.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Такой email уже зарегестрирован'
            )

        validated_data = obj.model_dump()
        query = (
            insert(self.model)
            .values(
                email=validated_data['email'],
                hashed_password=AuthService().get_password_hash(
                    validated_data['password']
                )
            )
            .returning(self.model)
        )
        result = await self.session.execute(query)
        return self.mapper.map_to_domain_entity(result.scalars().first())

    async def get_user_with_pass(self, email: str):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def update_avatar(self, user_id: int, image_id: int | None = None):
        query = (
            update(self.model)
            .filter_by(id=user_id)
            .values(image_id=image_id if image_id else None)
            .returning(self.model)
        )
        result = await self.session.execute(query)
        updated_obj = result.scalars().one_or_none()

        if updated_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{self.model.__name__} с id={filter_by} не найден'
            )

        return self.mapper.map_to_domain_entity(updated_obj)
