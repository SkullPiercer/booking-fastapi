from fastapi import HTTPException, status
from sqlalchemy import insert, select

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