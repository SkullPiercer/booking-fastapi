from app.api.schemas.facilities import FacilityDB
from app.db.crud.base import CRUDBase
from app.db.models.facilities import Facilities

class CRUDFacility(CRUDBase):
    model = Facilities
    schema = FacilityDB
