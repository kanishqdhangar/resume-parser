from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "resume_parser",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)

celery_app.conf.broker_use_ssl = {
    "ssl_cert_reqs": "CERT_NONE"
}

celery_app.conf.redis_backend_use_ssl = {
    "ssl_cert_reqs": "CERT_NONE"
}

import tasks