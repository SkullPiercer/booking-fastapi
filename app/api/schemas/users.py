from pydantic import BaseModel, EmailStr, SecretStr, model_validator


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr

    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError('Пароли не совпадают!')
        return self


class UserDBSchema(BaseModel):
    id: int
    email: str