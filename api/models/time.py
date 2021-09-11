import datetime


def datetime_now():
    return datetime.datetime.now().isoformat()[:19]
