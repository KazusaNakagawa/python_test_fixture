import datetime


def datetime_now():
    """ 現時刻表示を調整

    Sample
    ----------
    > '2021-09-12T22:45:51'
    """
    return datetime.datetime.now().isoformat()[:19]
