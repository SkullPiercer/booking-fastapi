from app.db.crud.base import CRUDBase
from app.db.crud.mappers.images import ImagesMapper
from app.db.models import Images


class CRUDImages(CRUDBase):
    model = Images
    mapper = ImagesMapper
