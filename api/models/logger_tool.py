import logging

from api.models import time

from pathlib import Path

LOGFILE_PATH = '../../log/'
LOG_FILE = 'bucket.log'

Path(LOGFILE_PATH).mkdir(exist_ok=True)
logging.basicConfig(filename=Path(f"{LOGFILE_PATH}{LOG_FILE}"), level=logging.INFO)
logger = logging.getLogger(__name__)


def error(action, status, bucket_name: str, ex):
    logger.error({
        'time': time.datetime_now(),
        'action': action,
        'status': status,
        'bucket name': bucket_name,
        'except': ex,
    })


def info(action, status, bucket_name: str):
    logger.info({
        'time': time.datetime_now(),
        'action': action,
        'status': status,
        'bucket name': bucket_name,
    })
