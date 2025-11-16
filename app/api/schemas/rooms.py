from pydantic import BaseModel, Field

class RoomCreateSchema(BaseModel):
    title: str = Field(..., max_length=90)
    description: str | None = Field(..., max_length=155)
    price: int = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    hotel_id: int = Field(..., gt=0)
