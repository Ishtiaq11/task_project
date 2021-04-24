from celery.decorators import task
from celery.utils.log import get_task_logger

from .email import send_comments_email

logger = get_task_logger(__name__)


@task(name="send_comments_email_task")
def send_comments_email_task(name, email,  quiz, comment):
    logger.info("Sent comments email")
    return send_comments_email(name, email,  quiz, comment)