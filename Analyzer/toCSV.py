#!/usr/bin/python

from csv_reader import CSVFile
from log_entry_analyzer import *

STATE = "state"

CONF_FILE = 'resources/conf'
RESULT_FILE = 'resources/aws_file.csv'

GET_TIME_TO_FIRST_STATEMENT = False
GET_ACTION_COUNT = False
GET_FILLING_TIME = False
FILTER_BY_OPERATION = False
FILTER_BY = ""


def read_conf():
    params = ""
    filter_by = ""
    with open(CONF_FILE, 'r') as f:
        contents = []
        for line in f:
            if line.startswith("#"):
                continue
            contents.append(line)
        if len(contents) < 0:
            raise ValueError("no data file name given")
        if len(contents) > 1:
            params = contents[1]
        if len(contents) > 2:
            filter_by = contents[2].strip()
    return contents[0].strip(), params, filter_by


def set_params(params, filter_by):
    global GET_TIME_TO_FIRST_STATEMENT, GET_ACTION_COUNT, GET_FILLING_TIME, FILTER_BY_OPERATION, FILTER_BY
    should_get_time_to_first_statement()
    should_get_action_count(params)
    should_get_application_filling_time(params)
    should_filter_by(filter_by)


def should_filter_by(filter_by):
    global FILTER_BY_OPERATION, FILTER_BY
    FILTER_BY_OPERATION = len(filter_by) > 0
    if FILTER_BY_OPERATION:
        FILTER_BY = filter_by
        print "filter by " + FILTER_BY


def should_get_application_filling_time(params):
    global GET_FILLING_TIME
    GET_FILLING_TIME = params.find(FILLING_TIME) >= 0
    if GET_FILLING_TIME:
        print FILLING_TIME


def should_get_action_count(params):
    global GET_ACTION_COUNT
    GET_ACTION_COUNT = params.find(ACTION_COUNT) >= 0
    if GET_ACTION_COUNT:
        print ACTION_COUNT


def should_get_time_to_first_statement():
    global GET_TIME_TO_FIRST_STATEMENT
    GET_TIME_TO_FIRST_STATEMENT = len(TIME) > 0
    if GET_TIME_TO_FIRST_STATEMENT:
        print TIME


def get_result_file_header():
    header = [APPLICATION_ID, MUNICIPALITY, TIME]
    if GET_ACTION_COUNT:
        header.append(ACTION_COUNT)
    if GET_FILLING_TIME:
        header.append(FILLING_TIME)
    return header


def write_as_csv(applications, header):
    lines = [",".join(header)]
    for application_id in applications:
        application = applications[application_id]
        line = ",".join(map(lambda h: str(application[h]), header))
        lines.append(line)
    with open('%s' % RESULT_FILE, 'w') as csv:
        csv.write("\n".join(lines))


def main():
    data_file, params, filter_by = read_conf()
    set_params(params, filter_by)
    csv_file = CSVFile([DATE, APPLICATION_ID, MUNICIPALITY, USER_ID, ROLE, ACTION, TARGET], data_file, ";")
    applications = to_applications(csv_file)

    columns2 = [APPLICATION_ID, MUNICIPALITY, PERMIT_TYPE, STATE, OPERATION, "operationId2", "operationId2", "createdDate", "submittedDate", "sentDate",
            "verdictGiven", "canceledDate", "isCancelled", "lon", "lat"]
    csv_file_2 = CSVFile(columns2, "/Users/liisasa/Dippa/applications-operative-on-20160914-20160918.csv", ";")
    joined = join(applications, csv_file_2)

    # Write results to csv -file
    write_as_csv(applications, get_result_file_header())
    write_as_csv(joined, get_result_file_header() + columns2)

    # Log statistics
    log_statistics(csv_file, applications)


def join(applications, csv_file):
    return inner_join(applications, csv_file)


def to_applications(csv_file):
    analyzer = LogEntryAnalyzer(GET_TIME_TO_FIRST_STATEMENT, GET_ACTION_COUNT, GET_FILLING_TIME, FILTER_BY_OPERATION, FILTER_BY)
    # Read applications
    applications = analyzer.to_applications(csv_file.rows)
    print "applications"
    # Rich data with filling time if wanted
    if GET_FILLING_TIME:
        applications = analyzer.to_applications_with_filling_time(applications)
    print "filling time"
    # Add the answering time to data
    if GET_TIME_TO_FIRST_STATEMENT:
        applications = analyzer.to_applications_with_time(applications)
    # Filter data with biggest municipalities
    print "time"
    if FILTER_BY_OPERATION:
        applications = analyzer.filter_applications_with_biggest_municipalities(applications, 5)
    print "filter"
    return applications


def log_statistics(csv_file, applications):
    print str(len(csv_file.rows)) + " rows in csv file"
    print str(len(applications)) + " applications"


if __name__ == "__main__":
    main()
