import datetime


def utc_date_compare_now_day(utc_str):
    """
    将utc时间戳转换为BJT，和凌晨做时间比较
    :param utc_str:
    :return:
    """
    if utc_str is None:
        return False

    utc_format = "%Y-%m-%dT%H:%M:%SZ"
    utc_time = datetime.datetime.strptime(utc_str, utc_format)
    bjt = utc_time + datetime.timedelta(hours=8)
    now = datetime.datetime.now()
    now_zero = datetime.datetime.now().replace(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
    return bjt > now_zero


def compare_now_day(utc_str):
    if utc_str is None:
        return False

    utc_format = "%Y-%m-%dT%H:%M:%SZ"
    utc_time = datetime.datetime.strptime(utc_str, utc_format)
    now = datetime.datetime.now()
    now_zero = datetime.datetime.now().replace(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
    return utc_time > now_zero
