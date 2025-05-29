from celery import Celery
from src.config import settings


task_queue = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks"
    ]
)