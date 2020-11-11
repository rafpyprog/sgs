"""
Time Serie manipulation
"""

import numpy as np
import pandas as pd

from . import api
from .common import to_datetime, apply_strict_range


def time_serie(ts_code: int, start: str, end: str, strict: bool = False) -> pd.Series:
    """
    Request a time serie data.

    :param ts_code: time serie code.
    :param start: start date (DD/MM/YYYY).
    :param end: end date (DD/MM/YYYY).
    :param strict: boolean to enforce a strict date range.

    :return: Time serie values as pandas Series indexed by date.
    :rtype: pandas.Series_

    Usage::

        >>> CDI = 12
        >>> ts = sgs.time_serie(CDI, start='02/01/2018', end='31/12/2018')
        >>> ts.head()
        2018-01-02    0.026444
        2018-01-03    0.026444
        2018-01-04    0.026444
        2018-01-05    0.026444
        2018-01-08    0.026444
    """

    values = []
    index = []
    for i in api.get_data(ts_code, start, end):
        values.append(i["valor"])
        index.append(to_datetime(i["data"], "pt"))

    # Transform empty strings in null values
    values = [np.nan if value == "" else value for value in values]

    ts = pd.Series(values, index, name=ts_code, dtype=np.float)

    if strict:
        ts = apply_strict_range(ts, start, end)

    return ts
