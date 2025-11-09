from fastapi import HTTPException, status

from pwdlib import PasswordHash
from sqlalchemy import insert

from app.api.schemas.users import UserDBSchema, UserCreateSchema
from app.db.crud.base import CRUDBase
from app.db.models import Users


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)


class CRUDUser(CRUDBase):
    model = Users
    schema = UserDBSchema

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
                hashed_password=get_password_hash(
                    validated_data['password'].get_secret_value()
                )
            )
            .returning(self.model)
        )
        result = await self.session.execute(query)
        return self.schema.model_validate(result.scalars().first(), from_attributes=True)