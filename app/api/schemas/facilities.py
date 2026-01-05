from pydantic import BaseModel


class FacilityCreateSchema(BaseModel):
    title: str


class FacilityDB(FacilityCreateSchema):
    id: int


class RoomFacilityCreateSchema(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilityDB(RoomFacilityCreateSchema):
    id: int
