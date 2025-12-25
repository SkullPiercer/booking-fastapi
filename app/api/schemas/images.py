from pydantic import BaseModel


class ImageCreateSchema(BaseModel):
    file_path: str | None = None

class ImageDBSchema(ImageCreateSchema):
    id: int