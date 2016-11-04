#!/usr/bin/python

from csv_reader import CSVFile
from log_entry_analyzer import *

CONF_FILE = 'resources/conf'
RESULT_FILE = 'resources/aws_file.csv'

GET_TIME_TO_FIRST_STATEMENT = False
GET_ACTION_COUNT = False
GET_FILLING_TIME = False
FILTER_BY_OPERATION = False
FILTER_BY_MUNICIPALITY = False
FILTER_BY = ""


def main():
    data_file, params, filter_by, join_file = read_conf()
    set_params(params, filter_by)
    csv_file = CSVFile([DATE, APPLICATION_ID, MUNICIPALITY, USER_ID, ROLE, ACTION, TARGET], data_file, ";")
    applications = to_applications(csv_file)

    applications = join(applications, join_file)

    tmp = {}
    for application_id in applications:
        application = applications[application_id]
        if application[SUBMITTED_DATE] is None:
            time_to_verdict = [(TIME_TO_VERDICT, "no_submit")]
        elif application[VERDICT_GIVEN] is None:
            time_to_verdict = [(TIME_TO_VERDICT, "no_verdict_give")]
        else:
            time = (application[VERDICT_GIVEN] - application[SUBMITTED_DATE]).seconds
            time_to_verdict = [(TIME_TO_VERDICT, time)]
        tmp[application_id] = dict(application.items() + time_to_verdict)

    applications = tmp

    # Write results to csv -file
    write_as_csv(applications, get_result_file_header())

    # Log statistics
    log_statistics(csv_file, applications)


def read_conf():
    data_file = ""
    join_file = ""
    params = ""
    filter_by = ""
    with open(CONF_FILE, 'r') as f:
        contents = read_file_and_skip_comments(f)
        if len(contents) < 0:
            raise ValueError("no data file name given")
        data_file, join_file = read_data_files(contents)
        if len(contents) > 1:
            params = contents[1]
        if len(contents) > 2:
            filter_by = contents[2].strip()
    return data_file, params, filter_by, join_file


def read_data_files(contents):
    join_file = ""
    data_files = contents[0].split()
    data_file = data_files[0].strip()
    if len(data_files) > 1:
        join_file = data_files[1].strip()
    return data_file, join_file


def read_file_and_skip_comments(f):
    contents = []
    for line in f:
        if line.startswith("#"):
            continue
        contents.append(line)
    return contents


def set_params(params, filter_by):
    should_get_time_to_first_statement()
    should_get_action_count(params)
    should_get_application_filling_time(params)
    should_filter_by_municipality(params)
    should_filter_by(filter_by)


def should_filter_by_municipality(params):
    global FILTER_BY_MUNICIPALITY
    FILTER_BY_MUNICIPALITY = params.find(MUNICIPALITY) >= 0
    if FILTER_BY_MUNICIPALITY:
        print MUNICIPALITY


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
    header = [APPLICATION_ID, MUNICIPALITY, TIME, TIME_TO_VERDICT]
    if GET_ACTION_COUNT:
        header.append(ACTION_COUNT)
    if GET_FILLING_TIME:
        header.append(FILLING_TIME)
    return header


def write_as_csv(applications, header, name=RESULT_FILE):
    lines = [",".join(header)]
    for application_id in applications:
        application = applications[application_id]
        line = ",".join(map(lambda h: str(application[h]), header))
        lines.append(line)
    with open('%s' % name, 'w') as csv:
        csv.write("\n".join(lines))


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
    if FILTER_BY_MUNICIPALITY:
        applications = analyzer.filter_applications_with_biggest_municipalities(applications, 5)
    print "filter"
    return applications


def join(applications, join_file):
    if join_file != "":
        columns2 = [APPLICATION_ID, MUNICIPALITY, PERMIT_TYPE, STATE, OPERATION, "operationId2", "operationId2", "createdDate", SUBMITTED_DATE, "sentDate",
                    VERDICT_GIVEN, "canceledDate", "isCancelled", "lon", "lat"]
        csv_file_2 = CSVFile(columns2, join_file, ";")
        applications = inner_join(applications, csv_file_2)
        write_as_csv(applications, [APPLICATION_ID, FILLING_TIME, MUNICIPALITY, VERDICT_GIVEN, SUBMIT_APPLICATION, SUBMITTED_DATE], "resources/joined.csv")

    return applications


def log_statistics(csv_file, applications):
    print str(len(csv_file.rows)) + " rows in csv file"
    print str(len(applications)) + " applications"


if __name__ == "__main__":
    main()
