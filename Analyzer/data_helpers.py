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


def inner_join(applications, applications2):
    joined_applications = {}
    for key in applications.keys():
        if applications2.has_key(key):
            joined_applications[key] = merge_dicts(applications[key], applications2[key])
    return joined_applications


def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
