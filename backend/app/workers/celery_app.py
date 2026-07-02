import asyncio

from celery import Celery
from celery.signals import worker_process_init

from app.core.config import settings
from app.database.mongodb import connect_to_mongodb

celery_app = Celery(
    "pdf_chat",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.imports = (
    "app.workers.pdf_tasks",
)

worker_loop = None


@worker_process_init.connect
def init_worker(**kwargs):
    global worker_loop

    worker_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(worker_loop)

    worker_loop.run_until_complete(connect_to_mongodb())