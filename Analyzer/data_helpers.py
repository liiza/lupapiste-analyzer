from itertools import groupby

from cell_names import *
from math import log

from cell_names import MUNICIPALITY_ID, MONTH, OPERATION, RUNNING_MONTH, TIME_TO_VERDICT


def get_time_diff_as(applications, start, end, param, log):
    applications_with_time = {}
    for application_id in applications:
        application = applications[application_id]
        if end not in application or start not in application:
            continue
        if not application[start] or not application[end]:
            continue
        if application[end] < application[start]:
            continue
        delta = application[end] - application[start]
        diff = delta.total_seconds()
        time = to_log(diff) if log else diff
        applications_with_time[application_id] = dict(application.items() + [(param, time)])
    return applications_with_time


def inner_join(applications, csv_file):
    joined_applications = {}
    for row in csv_file.rows:
        if row[APPLICATION_ID] in applications:
            joined_applications[row[APPLICATION_ID]] = merge_dicts(applications[row[APPLICATION_ID]], row)
    return joined_applications


def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def to_log(num):
    if num == 0:
        return 0
    return log(float(num))


def grouped_by(rows, target, param):
    sorted_by = sorted(map(lambda x: (x[target], x[param]), rows), key=lambda entry: entry[0])
    return groupby(sorted_by, lambda x: x[0])


def grouped_by_municipality(rows, param):
    return grouped_by(rows, MUNICIPALITY_ID, param)


def grouped_by_month(rows, param):
    sorted_by = sorted(map(lambda x: (x[MONTH], x[param]), rows), key=lambda entry: int(entry[0]))
    return groupby(sorted_by, lambda x: x[0])


def grouped_by_operation(rows, param):
    return grouped_by(rows, OPERATION, param)


def applications_grouped_by_running_month(file_rows):
    applications_per_running_month = []
    months = []
    grouped = grouped_by(file_rows, RUNNING_MONTH, TIME_TO_VERDICT)
    for key, group in grouped:
        verdict_times_per_month = map(lambda t: t[1], group)
        applications_per_running_month.append(len(verdict_times_per_month))
        months.append(key)
    return months, applications_per_running_month
