from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.api.dep.db import DBDep
from app.api.schemas.facilities import FacilityCreateSchema
from app.api.tasks_app.tasks import test_task


router = APIRouter()


@router.get("/")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    return await db.facility.get_list()


@router.post("/")
async def create_facility(db: DBDep, new_facility: FacilityCreateSchema):
    test_task.delay()
    _new_facility = await db.facility.create(new_facility)
    await db.commit()
    return _new_facility


@router.post("/bulk")
async def create_facilities(
    db: DBDep, new_facilities: list[FacilityCreateSchema]
):
    _new_facilities = await db.facility.create_bulk(new_facilities)
    await db.commit()
    return _new_facilities
