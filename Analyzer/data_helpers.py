

def diff(applications, start, end, param):
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
