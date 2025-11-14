from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash

from app.core.config import get_settings

settings = get_settings()


class AuthService():
    password_hash = PasswordHash.recommended()

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)


    def get_password_hash(self, password):
        return self.password_hash.hash(password)


    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = (
            datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode['exp'] = expire
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    
    def decode_access_token(self, data: str) -> dict:
        try:
            return jwt.decode(data, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Перезайдите в систему!'
            )