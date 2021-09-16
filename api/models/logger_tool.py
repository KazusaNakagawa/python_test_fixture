import logging

from api.models import time
from config import const

from pathlib import Path

# CREATE DIR
Path(const.LOGFILE_PATH).mkdir(exist_ok=True)
Path(const.TMP_PATH).mkdir(exist_ok=True)

logging.basicConfig(filename=Path(f"{const.LOGFILE_PATH}{const.LOG_FILE}"), level=logging.INFO)
logger = logging.getLogger(__name__)


def error(action, status, bucket_name: str, ex):
    logger.error({
        'time': time.datetime_now(),
        'action': action,
        'status': status,
        'bucket name': bucket_name,
        'except': ex,
    })


def info(action, status, bucket_name: str, data=None):
    logger.info({
        'time': time.datetime_now(),
        'action': action,
        'status': status,
        'bucket name': bucket_name,
        'data': data,
    })
