""" Module contains functions that are used to format, transform or classify date-time presented in a synergy format """

__author__ = 'Bohdan Mushkevych'

import calendar

from datetime import datetime, timedelta
from synergy.system.time_qualifier import *

SYNERGY_HOURLY_PATTERN = '%Y%m%d%H'
SYNERGY_SESSION_PATTERN = '%Y%m%d%H%M%S'


def define_pattern(timeperiod):
    if len(timeperiod) > 10:
        return SYNERGY_SESSION_PATTERN

    has_year = False
    has_month = False
    has_day = False
    has_hour = False

    for index in range(0, len(timeperiod)):
        if 0 <= index < 4 and timeperiod[index] != '0':
            has_year = True
        elif 4 <= index < 6 and timeperiod[index] != '0':
            has_month = True
        elif 6 <= index < 8 and timeperiod[index] != '0':
            has_day = True
        elif index >= 8 and timeperiod[index] != '0':
            has_hour = True

    pattern = ''
    if has_year:
        pattern += '%Y'
    else:
        pattern += '0000'
    if has_month:
        pattern += '%m'
    else:
        pattern += '00'
    if has_day:
        pattern += '%d'
    else:
        pattern += '00'
    if has_hour:
        pattern += '%H'
    else:
        pattern += '00'

    return pattern


def raw_to_session(timestamp):
    """ :param timestamp: <float> from time.time() output
    :return string in YYYYMMDDHHmmSS format"""
    t = datetime.utcfromtimestamp(timestamp)
    return t.strftime(SYNERGY_SESSION_PATTERN)


def session_to_hour(timestamp):
    """:param timestamp: as string in YYYYMMDDHHmmSS format
    :return string in YYYYMMDDHH format"""
    t = datetime.strptime(timestamp, SYNERGY_SESSION_PATTERN)
    return t.strftime(SYNERGY_HOURLY_PATTERN)


def hour_to_day(timeperiod):
    """:param timeperiod: as string in YYYYMMDDHH format
    :return string in YYYYMMDD00 format"""
    t = datetime.strptime(timeperiod, SYNERGY_HOURLY_PATTERN)
    return t.strftime('%Y%m%d00')


def day_to_month(timeperiod):
    """:param timeperiod: as string in YYYYMMDD00 format
    :return string in YYYYMM0000 format"""
    t = datetime.strptime(timeperiod, '%Y%m%d00')
    return t.strftime('%Y%m0000')


def month_to_year(timeperiod):
    """:param timeperiod: as string in YYYYMM0000 format
    :return string in YYYY000000 format"""
    t = datetime.strptime(timeperiod, '%Y%m0000')
    return t.strftime('%Y000000')


def actual_timeperiod(time_qualifier):
    """ method receives process' time qualifier (hourly/daily/monthly/yearly)
    :return string representing current datetime (utc now) in requested Synergy Date format """
    return datetime_to_synergy(time_qualifier, datetime.utcnow())


def increment_timeperiod(time_qualifier, timeperiod, delta=1):
    """ method performs simple increment/decrement of the timeperiods
    For instance: 2010010119 with delta=1 -> 2010010120
    Or 2010010000 with delta=-1 -> 2009120000, etc"""

    pattern = define_pattern(timeperiod)
    t = datetime.strptime(timeperiod, pattern)

    if time_qualifier == QUALIFIER_HOURLY:
        t = t + timedelta(hours=delta)
        return t.strftime('%Y%m%d%H')

    elif time_qualifier == QUALIFIER_DAILY:
        t = t + timedelta(days=delta)
        return t.strftime('%Y%m%d00')

    elif time_qualifier == QUALIFIER_MONTHLY:
        yearly_increment = abs(delta) // 12
        yearly_increment = yearly_increment if delta >= 0 else -yearly_increment
        monthly_increment = delta - yearly_increment * 12

        if t.month + monthly_increment > 12:
            new_month = t.month + monthly_increment - 12
            new_year = t.year + yearly_increment + 1
            t = t.replace(year=new_year, month=new_month)
        elif t.month + monthly_increment < 1:
            new_month = t.month + monthly_increment + 12
            new_year = t.year + yearly_increment - 1
            t = t.replace(year=new_year, month=new_month)
        else:
            t = t.replace(month=t.month + monthly_increment)
        return t.strftime('%Y%m0000')

    elif time_qualifier == QUALIFIER_YEARLY:
        t = t.replace(year=t.year + delta)
        return t.strftime('%Y000000')
    else:
        raise ValueError('unknown time qualifier: %s' % time_qualifier)


def cast_to_time_qualifier(time_qualifier, timeperiod):
    """ method casts given timeperiod accordingly to time qualifier.
    For example, will cast session time format of 20100101193412 to 2010010119 with QUALIFIER_HOURLY """

    if time_qualifier == QUALIFIER_HOURLY:
        date_format = SYNERGY_HOURLY_PATTERN
    elif time_qualifier == QUALIFIER_DAILY:
        date_format = '%Y%m%d00'
    elif time_qualifier == QUALIFIER_MONTHLY:
        date_format = '%Y%m0000'
    elif time_qualifier == QUALIFIER_YEARLY:
        date_format = '%Y000000'
    else:
        raise ValueError('unknown time qualifier: %s' % time_qualifier)

    pattern = define_pattern(timeperiod)
    t = datetime.strptime(timeperiod, pattern)
    return t.strftime(date_format)


def datetime_to_synergy(time_qualifier, dt):
    """ method parses datetime and returns Synergy Date"""
    if time_qualifier == QUALIFIER_HOURLY:
        date_format = SYNERGY_HOURLY_PATTERN
    elif time_qualifier == QUALIFIER_DAILY:
        date_format = '%Y%m%d00'
    elif time_qualifier == QUALIFIER_MONTHLY:
        date_format = '%Y%m0000'
    elif time_qualifier == QUALIFIER_YEARLY:
        date_format = '%Y000000'
    elif time_qualifier == QUALIFIER_REAL_TIME:
        date_format = SYNERGY_SESSION_PATTERN
    else:
        raise ValueError('unknown time qualifier: %s' % time_qualifier)
    return dt.strftime(date_format)


def synergy_to_datetime(time_qualifier, timeperiod):
    """ method receives timeperiod in Synergy format YYYYMMDDHH and convert it to UTC _naive_ datetime"""
    if time_qualifier == QUALIFIER_HOURLY:
        date_format = SYNERGY_HOURLY_PATTERN
    elif time_qualifier == QUALIFIER_DAILY:
        date_format = '%Y%m%d00'
    elif time_qualifier == QUALIFIER_MONTHLY:
        date_format = '%Y%m0000'
    elif time_qualifier == QUALIFIER_YEARLY:
        date_format = '%Y000000'
    elif time_qualifier == QUALIFIER_REAL_TIME:
        date_format = SYNERGY_SESSION_PATTERN
    else:
        raise ValueError('unknown time qualifier: %s' % time_qualifier)
    return datetime.strptime(timeperiod, date_format).replace(tzinfo=None)


def session_to_epoch(timestamp):
    """ converts Synergy Timestamp for session to UTC zone seconds since epoch """
    utc_timetuple = datetime.strptime(timestamp, SYNERGY_SESSION_PATTERN).replace(tzinfo=None).utctimetuple()
    return calendar.timegm(utc_timetuple)


if __name__ == '__main__':
    pass
