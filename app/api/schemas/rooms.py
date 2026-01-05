from pydantic import BaseModel, Field

from app.api.schemas.facilities import FacilityDB


class RoomsRequestSchema(BaseModel):
    title: str = Field(..., max_length=90)
    description: str | None = Field(None, max_length=155)
    price: int = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    facilities_ids: list[int] | None = None


class RoomsCreateSchema(BaseModel):
    hotel_id: int = Field(..., gt=0)
    title: str = Field(..., max_length=90)
    description: str | None = Field(None, max_length=155)
    price: int = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class RoomsDBSchema(RoomsCreateSchema):
    id: int


class RoomsPutSchema(RoomsCreateSchema):
    pass


class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None, max_length=90)
    description: str | None = Field(None, max_length=155)
    price: int | None = Field(None, ge=0)
    quantity: int | None = Field(None, ge=0)
    facilities_ids: list[int] | None = None


class RoomsPatchSchema(BaseModel):
    hotel_id: int | None = Field(None, gt=0)
    title: str | None = Field(None, max_length=90)
    description: str | None = Field(None, max_length=155)
    price: int | None = Field(None, ge=0)
    quantity: int | None = Field(None, ge=0)


class RoomWithRels(RoomsDBSchema):
    facilities: list[FacilityDB]
