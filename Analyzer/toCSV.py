#!/usr/bin/python

from log_entry_analyzer import *

GET_ACTION_COUNT = False
GET_FILLING_TIME = False
FILTER_BY_OPERATION = False
FILTER_BY = ""


def read_conf():
    params = ""
    filter_by = ""
    with open('conf', 'r') as f:
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


def to_csv(applications):
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
    data_file, params, filter_by = read_conf()
    set_params(params, filter_by)
    print "log_entries"
    analyzer = LogEntryAnalyzer(GET_ACTION_COUNT, GET_FILLING_TIME, FILTER_BY_OPERATION, FILTER_BY)
    log_entries = analyzer.to_log_entries(open(data_file, 'r'))
    print "applications"
    applications = analyzer.to_applications(log_entries)
    if GET_FILLING_TIME:
        applications = analyzer.to_applications_with_filling_time(applications)
    print "time"
    applications_with_time = analyzer.to_applications_with_time(applications)
    print len(log_entries)
    print len(applications)
    print len(applications_with_time)
    print "tocsv"
    to_csv(applications_with_time)


if __name__ == "__main__":
    main()
