import asyncio

from app.services.pdf_processing_service import pdf_processing_service
from app.workers.celery_app import celery_app


from app.workers.utils import run_async


@celery_app.task(
    name="app.workers.pdf_tasks.process_pdf",
    bind=True,
)
def process_pdf(self, document_id: str):
    run_async(
        pdf_processing_service.process(document_id)
    )