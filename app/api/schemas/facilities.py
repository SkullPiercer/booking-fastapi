from pydantic import BaseModel

class FacilityCreateSchema(BaseModel):
    title: str


class FacilityDB(FacilityCreateSchema):
    id: int
