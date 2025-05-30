from celery import Celery
from src.config import settings


task_queue = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks"
    ]
)

task_queue.conf.beat_schedule = {
    "kot_nasral": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}