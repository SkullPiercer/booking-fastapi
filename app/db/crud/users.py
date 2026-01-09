import logging

from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from app.api.exceptions.timed_base import ObjectExistsException
from app.api.schemas.users import UserCreateSchema
from app.core.user import AuthService
from app.db.crud.base import CRUDBase
from app.db.crud.mappers.users import UsersMapper
from app.db.models import Users


class CRUDUser(CRUDBase):
    model = Users
    mapper = UsersMapper

    async def create(self, obj: UserCreateSchema):
        try:
            validated_data = obj.model_dump()
            query = (
                insert(self.model)
                .values(
                    email=validated_data["email"],
                    hashed_password=AuthService().get_password_hash(
                        validated_data["password"]
                    ),
                )
                .returning(self.model)
            )
            result = await self.session.execute(query)
            return self.mapper.map_to_domain_entity(result.scalars().first())
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                logging.error(
                    f"Ошибка обработки запроса: {type(ex.orig.__cause__)=}\n"
                    f"При данных {obj.email}"
                )
                raise ObjectExistsException from ex
            else:
                logging.error(
                    f"Неизвестная ошибка: {type(ex.orig.__cause__)=}"
                    f"Данные: {obj.email}"

                )
                raise ex

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
                detail=f"{self.model.__name__} с id={user_id} не найден",
            )

        return self.mapper.map_to_domain_entity(updated_obj)
