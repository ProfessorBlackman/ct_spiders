from celery import Celery
from decouple import config

app = Celery(
    'ct_spider_i',
    broker=config('CELERY_BROKER_URL'),
    backend=config('CELERY_RESULT_BACKEND'),
    include=['ct_spider_i.tasks'],
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],

)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)
