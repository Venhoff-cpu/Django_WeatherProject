import datetime
import pandas as pd


def unix_to_datetime(unix_date):
    """
    unction for converting unix date format into datetime format
    :param unix_date: date presented in unix format
    :return: date in YYYY-mm-dd format
    """
    date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%Y-%m-%d")
    return date
