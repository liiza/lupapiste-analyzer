#!/usr/bin/python
from datetime import datetime

from conf_reader import Conf
from csv_reader import CSVFile
from log_entry_analyzer import *

RESULT_FILE = 'resources/aws_file.csv'


def main():
    conf = Conf()
    params = conf.get_params()
    csv_file = CSVFile([DATE, APPLICATION_ID, MUNICIPALITY, USER_ID, ROLE, ACTION, TARGET], conf.data_file, ";")
    applications = to_applications(csv_file, conf, params)

    # Write results to csv -file
    write_as_csv(applications, get_result_file_header(params))

    # Log statistics
    log_statistics(csv_file, applications)


def to_applications(csv_file, conf, params):
    analyzer = LogEntryAnalyzer(params.get_time_to_first_statement,
                                params.get_action_count,
                                params.application_filling_time,
                                params.filter_by_operation,
                                params.filter_by,
                                params.calculate_attachments)
    # Read applications
    applications = analyzer.to_applications(csv_file.rows)
    applications = join(applications, conf.join_file)

    # Filter by operation
    if params.filter_by_operation:
        applications = analyzer.filter_applications_by_operation(applications, params.filter_by)

    # Filter data with biggest municipalities
    if params.filter_by_municipality:
        before = datetime.now()
        applications = analyzer.filter_applications_with_biggest_municipalities(applications, 5)
        print (datetime.now() - before).seconds

    # Add time to verdict
    if params.time_to_verdict:
        applications = analyzer.to_applications_with_time_to_verdict(applications, params.logarithmic_numbers)

    # Rich data with filling time if wanted
    if params.application_filling_time:
        applications = analyzer.to_applications_with_filling_time(applications, params.logarithmic_numbers)

    # Add time to first statement
    if params.get_time_to_first_statement:
        applications = analyzer.to_applications_with_time_to_first_statement(applications, params.logarithmic_numbers)

    # Add the month application was created
    if params.month:
        applications = analyzer.to_applications_with_start_month(applications)

    if params.running_month:
        applications = analyzer.to_applications_with_running_month(applications)
    return applications


def join(applications, join_file):
    if join_file != "":
        columns2 = [APPLICATION_ID, MUNICIPALITY, PERMIT_TYPE, STATE, OPERATION,
                    "operationId2", "operationId3", "operations", CREATED_DATE, SUBMITTED_DATE, "sentDate",
                    VERDICT_GIVEN, "canceledDate", "isCancelled", "lon", "lat"]
        csv_file_2 = CSVFile(columns2, join_file, ";")
        applications = inner_join(applications, csv_file_2)
        write_as_csv(applications, [APPLICATION_ID, MUNICIPALITY, VERDICT_GIVEN, SUBMITTED_DATE], "resources/joined.csv")

    return applications


def get_result_file_header(params):
    header = [APPLICATION_ID, MUNICIPALITY]
    if params.get_action_count:
        header.append(ACTION_COUNT)
    if params.application_filling_time:
        header.append(FILLING_TIME)
    if params.get_time_to_first_statement:
        header.append(TIME_TO_STATEMENT)
    if params.filter_by_operation:
        header.append(OPERATION)
    if params.month:
        header.append(MONTH)
    if params.time_to_verdict:
        header.append(TIME_TO_VERDICT)
    if params.calculate_attachments:
        header.append(ATTACHMENT_COUNT)
    if params.running_month:
        header.append(RUNNING_MONTH)
    return header


def write_as_csv(applications, header, name=RESULT_FILE):
    lines = [",".join(header)]
    for application_id in applications:
        application = applications[application_id]
        line = ",".join(map(lambda h: str(application[h]), header))
        lines.append(line)
    with open('%s' % name, 'w') as csv:
        csv.write("\n".join(lines))


def log_statistics(csv_file, applications):
    print str(len(csv_file.rows)) + " rows in csv file"
    print str(len(applications)) + " applications"


if __name__ == "__main__":
    main()
