from datetime import date

from pydantic import BaseModel, Field

class BookingRequestSchema(BaseModel):
    room_id: int = Field(..., gt=0)
    date_from: date
    date_to: date
    price: int


class BookingCreateSchema(BookingRequestSchema):
    user_id: int

class BookingDBSchema(BookingCreateSchema):
    id: int