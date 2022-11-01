"""
Transform datetimes from string to decimal.

Examples
--------
time_float()
time_float(['2017-06-29 23:59:59.1234', '2017-12-01 00:15:21.1234'])
time_double()

Notes
-----
Similar to time_double.pro in IDL SPEDAS.

"""

from dateutil import parser
from datetime import datetime, timezone
import numpy as np
from collections.abc import Iterable


def time_float_one(s_time=None):
    """
    Transform one datetime from string to decimal.

    Parameters
    ----------
    s_time : str, optional
        Input string.
        The default is None, which returns Now.

    Returns
    -------
    float
        Output time.

    """
    if s_time is None:
        s_time = str(datetime.now())

    if isinstance(s_time, (int, float, np.integer, np.float64)):
        return float(s_time)

    try:
        in_datetime = parser.isoparse(s_time)
    except ValueError:
        in_datetime = parser.parse(s_time)

    float_time = in_datetime.replace(tzinfo=timezone.utc).timestamp()

    return float_time


def time_float(str_time=None):
    """
    Transform a list of datetimes from string to decimal.

    Parameters
    ----------
    str_time : str/list of str, optional
        Input times. The default is None.

    Returns
    -------
    list of float
        Output times as floats.

    """
    if str_time is None:
        return time_float_one()
    else:
        if isinstance(str_time, str):
            return time_float_one(str_time)
        else:
            time_list = list()
            if isinstance(str_time, Iterable):
                for t in str_time:
                    time_list.append(time_float_one(t))
                return time_list
            else:
                return time_float_one(str_time)


def time_double(str_time=None):
    """
    Transform a list of datetimes from string to decimal.

    Same as time_float.

    Parameters
    ----------
    str_time : str/list of str, optional
        Input times. The default is None.

    Returns
    -------
    list of float
        Output times as floats.

    """
    return time_float(str_time)






"""
Transform datetimes from decimal to string.

Examples
--------
time_string()
time_string([1498780799.1234, 1512087321.1234])

Notes
-----
Compare to https://www.epochconverter.com/

"""

def time_string_one(float_time=None, fmt=None):
    """
    Transform a single float daytime value to string.

    Parameters
    ----------
    float_time : float, optional
        Input time.
        The default is None, which returns the time now.
    fmt : float, optional
        Time format.
        The default is None, which uses '%Y-%m-%d %H:%M:%S.%f'.

    Returns
    -------
    str
        Datetime as string.

    """
    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S.%f'

    if float_time is None:
        str_time = datetime.now().strftime(fmt)
    else:
        str_time = datetime.utcfromtimestamp(float_time).strftime(fmt)

    return str_time


def time_string(float_time=None, fmt=None):
    """
    Transform a list of float daytime values to a list of strings.

    Parameters
    ----------
    float_time: float/list of floats, optional
        Input time.
        The default is None, which returns the time now.
    fmt: str, optional
        Time format.
        The default is None, which uses '%Y-%m-%d %H:%M:%S.%f'.

    Returns
    -------
    list of str
        Datetimes as string.

    """
    if float_time is None:
        return time_string_one(None, fmt)
    else:
        if isinstance(float_time, (int, float)):
            return time_string_one(float_time, fmt)
        else:
            time_list = list()
            for t in float_time:
                time_list.append(time_string_one(t, fmt))
            return time_list


def time_datetime(time=None, tz=None):
    """Find python datetime.

    Transform a list of float daytime values to a list of pythonic
        'datetime.datetime' values.

    Parameters
    ----------
    time: float/list of floats or str/list of str, optional
        Input time.
        The default is None, which returns the time now.

    Returns
    -------
    list of datetime.datetime
        Datetimes as `datetime.datetime`.

    """
    if tz == None:
        tz = timezone.utc

    if time is None:
        return datetime.now()

    if isinstance(time, str):
        return time_datetime(time_float(time))

    if isinstance(time, (int, float)):
        return datetime.fromtimestamp(time, tz=tz)

    return [time_datetime(_time) for _time in time]
