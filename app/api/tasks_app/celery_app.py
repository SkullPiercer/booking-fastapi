from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_inst = Celery(
    "fastapi-tasks",
    broker=settings.CELERY_URL,
    include=["app.api.tasks_app.tasks"],
)

celery_inst.conf.beat_schedule = {
    "luboe-nazvanie": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}
