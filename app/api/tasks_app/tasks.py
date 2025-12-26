import asyncio
from time import sleep

from app.api.dep.db import DBManager
from app.api.tasks_app.celery_app import celery_inst
from app.core.db import async_session_maker_null_pool


@celery_inst.task
def test_task():
    sleep(2)
    return 1


async def get_bookings_with_today_checkin_helper():
    print("Я ЗАПУСКАЮСЬ")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_inst.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
