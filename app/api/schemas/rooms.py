from pydantic import BaseModel, Field


class RoomsRequestSchema(BaseModel):
    title: str = Field(..., max_length=90)
    description: str | None = Field(None, max_length=155)
    price: int = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class RoomsCreateSchema(RoomsRequestSchema):
    hotel_id: int = Field(..., gt=0)


class RoomsDBSchema(RoomsCreateSchema):
    id: int


class RoomsPutSchema(RoomsCreateSchema):
    pass


class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None, max_length=90)
    description: str | None = Field(None, max_length=155)
    price: int | None = Field(None, ge=0)
    quantity: int | None = Field(None, ge=0)


class RoomsPatchSchema(RoomsPatchRequest):
    hotel_id: int | None = Field(None, gt=0)
