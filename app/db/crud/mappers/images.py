from app.api.schemas.images import ImageDBSchema
from app.db.crud.mappers.base import DataMapper
from app.db.models import Images


class ImagesMapper(DataMapper):
    model = Images
    schema = ImageDBSchema
