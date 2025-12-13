from fastapi import APIRouter

from app.api.dep.db import DBDep
from app.api.schemas.facilities import FacilityCreateSchema

router = APIRouter()

@router.get('/')
async def get_all_facilities(
        db: DBDep
):
    return await db.facility.get_list()


@router.post('/')
async def create_facility(
        db: DBDep,
        new_facility: FacilityCreateSchema
):
    _new_facility = await db.facility.create(new_facility)
    await db.commit()
    return _new_facility