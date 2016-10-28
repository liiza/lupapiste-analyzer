#!/usr/bin/python

from datetime import datetime

DATE = 'date'
USER_ID = 'userId'
ROLE = 'role'
MUNICIPALITY = 'municipality'
APPLICATION_ID = 'applicationId'
ACTION = 'action'
TARGET = 'target'
IS_INFO_REQUEST = "isInfoRequest"
OPERATION = "operation"
COLUMNS = [DATE, APPLICATION_ID, IS_INFO_REQUEST, OPERATION, MUNICIPALITY, USER_ID, ROLE, ACTION, TARGET]

SUBMIT_APPLICATION = 'submit-application'
GIVE_STATEMENT = 'give-statement'
APPLICANT = 'applicant'
AUTHORITY = 'authority'

START_TIME = 'start-time'
ACTION_COUNT = 'action-count'
TIME = 'time'
FILLING_TIME = 'filling-time'

GET_ACTION_COUNT = False
GET_FILLING_TIME = False
FILTER_BY_OPERATION = False


def to_date(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')


def to_cells(line):
    chunks = line.split(";")
    return {DATE: to_date(chunks[COLUMNS.index(DATE)]),
            ROLE: chunks[COLUMNS.index(ROLE)],
            MUNICIPALITY: chunks[COLUMNS.index(MUNICIPALITY)],
            APPLICATION_ID: chunks[COLUMNS.index(APPLICATION_ID)],
            ACTION: chunks[COLUMNS.index(ACTION)],
            OPERATION: chunks[COLUMNS.index(OPERATION)]}


def to_log_entries(data):
    header = True
    data_entries = []
    for line in data:
        if header:
            header = False
            continue
        data_entries.append(to_cells(line))
    return data_entries


def get_or_create_application(application_id, applications, log_entry):
    if applications.has_key(application_id):
        return applications[application_id]
    else:
        application = {MUNICIPALITY: log_entry[MUNICIPALITY]}
        if GET_ACTION_COUNT:
            application[ACTION_COUNT] = 0
        if GET_FILLING_TIME:
            application[START_TIME] = log_entry[DATE]
        applications[application_id] = application
        return application


def to_applications(log_entries):
    applications = {}
    for log_entry in log_entries:
        if FILTER_BY_OPERATION and log_entry[OPERATION] != 'pientalo':
            continue

        application = get_or_create_application(log_entry[APPLICATION_ID], applications, log_entry)

        if log_entry[ACTION] == SUBMIT_APPLICATION and log_entry[ROLE] == APPLICANT:
            if not application.has_key(SUBMIT_APPLICATION) or application[SUBMIT_APPLICATION] > log_entry[DATE]:
                application[SUBMIT_APPLICATION] = log_entry[DATE]

        elif log_entry[ACTION] == GIVE_STATEMENT and log_entry[ROLE] == AUTHORITY:
            if not application.has_key(GIVE_STATEMENT) or application[GIVE_STATEMENT] > log_entry[DATE]:
                application[GIVE_STATEMENT] = log_entry[DATE]

        elif GET_ACTION_COUNT:
            application[ACTION_COUNT] += 1

        if GET_FILLING_TIME:
            if not application.has_key(START_TIME) or application[START_TIME] > log_entry[DATE]:
                application[START_TIME] = log_entry[DATE]

    return applications


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


def to_applications_with_filling_time(applications):
    return diff(applications, START_TIME, SUBMIT_APPLICATION, FILLING_TIME)


def to_applications_with_time(applications):
    return diff(applications, SUBMIT_APPLICATION, GIVE_STATEMENT, TIME)


def read_conf():
    with open('conf', 'r') as f:
        contents = []
        for line in f:
            if line.startswith("#"):
                continue
            contents.append(line)
        if len(contents) < 0:
            raise ValueError("no data file name given")
        params = ""
        if len(contents) > 1:
            params = contents[1]
    return contents[0].strip(), params


def set_params(params):
    global GET_ACTION_COUNT, GET_FILLING_TIME, FILTER_BY_OPERATION
    GET_ACTION_COUNT = params.find(ACTION_COUNT) >= 0
    GET_FILLING_TIME = params.find(FILLING_TIME) >= 0
    FILTER_BY_OPERATION = params.find("filter") >= 0
    if GET_ACTION_COUNT:
        print ACTION_COUNT
    if GET_FILLING_TIME:
        print FILLING_TIME
    if FILTER_BY_OPERATION:
        print "filter"


def to_CSV(applications):
    lines = []
    header = [MUNICIPALITY, TIME]
    if GET_ACTION_COUNT:
        header.append(ACTION_COUNT)
    if GET_FILLING_TIME:
        header.append(FILLING_TIME)
    lines.append(",".join(header))
    for application_id in applications:
        application = applications[application_id]
        line = ",".join(map(str, [application[MUNICIPALITY], application[TIME]]))
        if GET_ACTION_COUNT:
            line += "," + str(application[ACTION_COUNT])
        if GET_FILLING_TIME:
            line += "," + str(application[FILLING_TIME])
        lines.append(line)

    with open('aws_file.csv', 'w') as csv:
        csv.write("\n".join(lines))


def main():
    data_file, params = read_conf()
    set_params(params)
    print "log_entries"
    log_entries = to_log_entries(open(data_file, 'r'))
    print "applications"
    applications = to_applications(log_entries)
    if GET_FILLING_TIME:
        applications = to_applications_with_filling_time(applications)
    print "time"
    applications_with_time = to_applications_with_time(applications)
    print len(log_entries)
    print len(applications)
    print len(applications_with_time)
    print "tocsv"
    to_CSV(applications_with_time)


if __name__ == "__main__":
    main()
