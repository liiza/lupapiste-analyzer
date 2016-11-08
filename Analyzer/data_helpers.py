from cell_names import *


def get_time_diff_as(applications, start, end, param):
    applications_with_time = {}
    for application_id in applications:
        application = applications[application_id]
        if not application.has_key(end) or not application.has_key(start):
            continue
        if application[end] < application[start]:
            continue
        time = (application[end] - application[start]).seconds
        applications_with_time[application_id] = dict(application.items() + [(param, time)])
    return applications_with_time


def inner_join(applications, csv_file):
    joined_applications = {}
    for row in csv_file.rows:
        if applications.has_key(row[APPLICATION_ID]):
            joined_applications[row[APPLICATION_ID]] = merge_dicts(applications[row[APPLICATION_ID]], row)
    return joined_applications


def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
