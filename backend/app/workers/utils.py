import app.workers.celery_app as celery_module


def run_async(coro):
    return celery_module.worker_loop.run_until_complete(coro)