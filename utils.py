#-*- coding: utf8 -*-
from datetime import datetime
from pytz import utc


def utc_timestamp_to_datetime(timestamp):
    """
    Converts the given timestamp to a datetime instance.

    :type timestamp: float
    :rtype: datetime
    """

    if timestamp is not None:
        return datetime.fromtimestamp(timestamp, utc)


def convert_period_job(job):
    job['next_timestamp'] = utc_timestamp_to_datetime(job['next_timestamp']).strftime("%Y-%m-%d %H:%M:%S")
    job['lastModified'] = job['lastModified'].strftime("%Y-%m-%d %H:%M:%S")
    return job


def convert_job_records(job):
    execute_records = []
    for record in job['execute_records']:
        record['report_timestamp'] = record['report_timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        execute_records.append(record)
    job['execute_records'] = execute_records
    return job