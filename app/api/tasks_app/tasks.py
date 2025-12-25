from time import sleep

from app.api.tasks_app.celery_app import celery_inst

@celery_inst.task
def test_task():
    sleep(2)
    return 1
