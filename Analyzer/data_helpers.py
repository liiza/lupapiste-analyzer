from cell_names import *
from math import log


def get_time_diff_as(applications, start, end, param):
    applications_with_time = {}
    for application_id in applications:
        application = applications[application_id]
        if not end in application or not start in application:
            continue
        if application[end] < application[start]:
            continue
        time = (application[end] - application[start]).seconds
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
    return log(int(num))
