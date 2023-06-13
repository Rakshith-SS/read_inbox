"""
    Commonly used functions are written here.
"""
from datetime import datetime


def convert_datetime(datetime_string: str) -> datetime:
    """
        Convert a String contain date,
        to datetime obj.

        Example:
            Input- Sat, 10 Jun 2023 22:16:03 +0530
            Output - 2023-06-10 22:16:03+05:30
    """
    date_format = "%a, %d %b %Y %H:%M:%S %z"
    if datetime_string.split()[-1] == 'GMT':
        date_format = "%a, %d %b %Y %H:%M:%S %Z"

    datetime_obj = datetime.strptime(datetime_string, date_format)
    return datetime_obj
