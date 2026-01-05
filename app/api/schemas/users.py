from pydantic import BaseModel, EmailStr, model_validator


class UserTokenSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(UserTokenSchema):
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают!")
        return self


class UserDBSchema(BaseModel):
    id: int
    email: str


class UserWithHashPass(BaseModel):
    hashed_password: str
