#!/usr/bin/python

from csv_reader import CSVFile
from log_entry_analyzer import *
from log_entry_analyzer import get_biggest_municipalities

CONF_FILE = 'resources/conf'
RESULT_FILE = 'resources/aws_file.csv'

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
    global GET_ACTION_COUNT, GET_FILLING_TIME, FILTER_BY_OPERATION, FILTER_BY
    GET_ACTION_COUNT = params.find(ACTION_COUNT) >= 0
    if GET_ACTION_COUNT:
        print ACTION_COUNT
    GET_FILLING_TIME = params.find(FILLING_TIME) >= 0
    if GET_FILLING_TIME:
        print FILLING_TIME
    FILTER_BY_OPERATION = len(filter_by) > 0
    if FILTER_BY_OPERATION:
        FILTER_BY = filter_by
        print "filter by " + FILTER_BY


def write_as_csv(applications):
    lines = []
    header = [APPLICATION_ID, MUNICIPALITY, TIME]
    if GET_ACTION_COUNT:
        header.append(ACTION_COUNT)
    if GET_FILLING_TIME:
        header.append(FILLING_TIME)
    lines.append(",".join(header))
    for application_id in applications:
        application = applications[application_id]
        line = ",".join(map(lambda h: str(application[h]), header))
        lines.append(line)

    with open('%s' % RESULT_FILE, 'w') as csv:
        csv.write("\n".join(lines))


def to_municipality_application_pair(applications):
    return lambda application_id: (applications[application_id][MUNICIPALITY], applications[application_id])


def main():
    data_file, params, filter_by = read_conf()
    set_params(params, filter_by)
    csv_file = CSVFile([DATE, APPLICATION_ID, IS_INFO_REQUEST, OPERATION, MUNICIPALITY, USER_ID, ROLE, ACTION, TARGET], data_file, ";")

    analyzer = LogEntryAnalyzer(GET_ACTION_COUNT, GET_FILLING_TIME, FILTER_BY_OPERATION, FILTER_BY)
    applications = analyzer.to_applications(csv_file.rows)
    if GET_FILLING_TIME:
        applications = analyzer.to_applications_with_filling_time(applications)
    applications_with_time = analyzer.to_applications_with_time(applications)

    biggest_municipalities = LogEntryAnalyzer.get_biggest_municipalities(applications_with_time, 5)

    log_statistics(applications, applications_with_time, biggest_municipalities, csv_file)
    write_as_csv(applications_with_time)


def log_statistics(applications, applications_with_time, biggest_municipalities, csv_file):
    print str(len(csv_file.rows)) + " rows in csv file"
    print str(len(applications)) + " applications"
    print str(len(applications_with_time)) + " applications with statement"
    print "Biggest municipalities and applications " + str(biggest_municipalities)


if __name__ == "__main__":
    main()
