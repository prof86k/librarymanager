from .celery import app
from celery.utils.log import get_task_logger
from accounts.emails import send_email_messages

logger = get_task_logger(__name__)

@app.task(name='testing_that_celery_works')
def we_are_testing_celery(email,message):
    'print that the celery is working correctly'
    logger.info('Celery has started to work properly')
    return send_email_messages(email,message)