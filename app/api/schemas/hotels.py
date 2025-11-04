from pydantic import BaseModel,Field, field_validator


class HotelCreateSchema(BaseModel):
    title: str = Field(..., min_length=4, max_length=20)
    location: str = Field(..., min_length=4, max_length=20)

    @field_validator('title', 'location')
    def no_empty_spaces(cls, value: str, field) -> str:
        if not value.strip():
            raise ValueError(f"Поле '{field.name}' не может быть пустым")
        return value


class HotelPutSchema(BaseModel):
    title: str
    location: str


class HotelPatchSchema(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
