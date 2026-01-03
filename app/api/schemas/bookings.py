from datetime import date

from pydantic import BaseModel, Field, ConfigDict

class BookingRequestSchema(BaseModel):
    room_id: int = Field(..., gt=0)
    date_from: date
    date_to: date


class BookingCreateSchema(BookingRequestSchema):
    user_id: int
    price: int


class BookingUpdateSchema(BaseModel):
    room_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None


class BookingDBSchema(BookingCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)