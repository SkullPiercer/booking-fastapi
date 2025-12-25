import json

from fastapi import APIRouter

from app.api.dep.db import DBDep
from app.api.schemas.facilities import FacilityCreateSchema
from app.api.tasks_app.tasks import test_task
from app.conectors.redis_connector import redis_manager


router = APIRouter()

@router.get('/')
async def get_all_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get('facilities')
    if facilities_from_cache is None:
        print('Идем за удобствами в бд')
        facilities = await db.facility.get_list()
        list_of_facilities = [f.model_dump() for f in facilities]
        await redis_manager.set('facilities', json.dumps(list_of_facilities), 10)
        return facilities
    return json.loads(facilities_from_cache)


@router.post('/')
async def create_facility(
        db: DBDep,
        new_facility: FacilityCreateSchema
):
    test_task.delay()
    _new_facility = await db.facility.create(new_facility)
    await db.commit()
    return _new_facility