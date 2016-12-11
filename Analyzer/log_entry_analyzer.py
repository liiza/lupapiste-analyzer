import operator
from itertools import groupby

from cell_names import *
from data_helpers import get_time_diff_as, merge_dicts


class LogEntryAnalyzer:
    def __init__(self, get_time_to_first_statement=False, get_action_count=False, get_filling_time=False, filter_by_operation=False, filter_by=None,
                 calculate_attachments=False):
        self.get_time_to_first_statement = get_time_to_first_statement
        self.get_action_count = get_action_count
        self.get_filling_time = get_filling_time
        self.filter_by_operation = filter_by_operation
        self.filter_by = filter_by
        self.calculate_attachments = calculate_attachments

    def to_applications(self, log_entries):
        applications = {}
        for log_entry in log_entries:
            application = self.get_or_create_application(log_entry[APPLICATION_ID], applications, log_entry)

            if START_TIME not in application or application[START_TIME] > log_entry[DATE_TIME]:
                application[START_TIME] = log_entry[DATE_TIME]

            if log_entry[ACTION] == SUBMIT_APPLICATION and log_entry[ROLE] == APPLICANT:
                # Application can be submitted several times we want the first one.
                if SUBMIT_APPLICATION not in application or application[SUBMIT_APPLICATION] > log_entry[DATE_TIME]:
                    application[SUBMIT_APPLICATION] = log_entry[DATE_TIME]

            if log_entry[ACTION] == GIVE_STATEMENT and log_entry[ROLE] == AUTHORITY:
                if GIVE_STATEMENT not in application or application[GIVE_STATEMENT] > log_entry[DATE_TIME]:
                    application[GIVE_STATEMENT] = log_entry[DATE_TIME]

            if self.calculate_attachments and log_entry[ACTION] == "upload-attachment":
                if ATTACHMENT_COUNT not in application:
                    application[ATTACHMENT_COUNT] = 0
                application[ATTACHMENT_COUNT] += 1

            if self.get_action_count and (SUBMIT_APPLICATION not in application or log_entry[DATE_TIME] < application[SUBMIT_APPLICATION]):
                if ACTION_COUNT not in application:
                    application[ACTION_COUNT] = 0
                application[ACTION_COUNT] += 1

        return applications

    @staticmethod
    def get_or_create_application(application_id, applications, log_entry):
        if application_id in applications:
            return applications[application_id]
        else:
            application = {APPLICATION_ID: log_entry[APPLICATION_ID], MUNICIPALITY_ID: log_entry[MUNICIPALITY_ID]}
            applications[application_id] = application
            application[ATTACHMENT_COUNT] = 0
            return application

    @staticmethod
    def get_biggest_municipalities(applications_with_time, amount):
        grouped_by_municipality = LogEntryAnalyzer.group_by_municipalities(applications_with_time)
        municipality_count_map = {}
        for key, group in grouped_by_municipality:
            municipality_count_map[key] = len(map(lambda x: x[1], group))
        return sorted(municipality_count_map.items(), key=operator.itemgetter(1), reverse=True)[:amount]

    @staticmethod
    def group_by_municipalities(applications_with_time):
        municipality_row_map = map(LogEntryAnalyzer.to_municipality_application_pair(applications_with_time), applications_with_time)
        sorted_by_municipality = sorted(municipality_row_map, key=lambda entry: entry[0])
        grouped_by_municipality = groupby(sorted_by_municipality, lambda entry: entry[0])
        return grouped_by_municipality

    @staticmethod
    def to_municipality_application_pair(applications):
        return lambda application_id: (applications[application_id][MUNICIPALITY_ID], applications[application_id])

    @staticmethod
    def to_applications_with_filling_time(applications, log):
        return get_time_diff_as(applications, START_TIME, SUBMIT_APPLICATION, FILLING_TIME, log)

    @staticmethod
    def to_applications_with_time_to_first_statement(applications, log):
        return get_time_diff_as(applications, SUBMIT_APPLICATION, GIVE_STATEMENT, TIME_TO_STATEMENT, log)

    @staticmethod
    def to_applications_with_time_to_verdict(applications, log):
        return get_time_diff_as(applications, SUBMIT_APPLICATION, VERDICT_GIVEN, TIME_TO_VERDICT, log)

    @staticmethod
    def filter_applications_with_biggest_municipalities(applications, amount):
        municipalities_and_applications_counts = LogEntryAnalyzer.get_biggest_municipalities(applications, amount)
        print "Biggest municipalities and applications " + str(municipalities_and_applications_counts)
        municipalities = map(lambda t: t[0], municipalities_and_applications_counts)
        return {k: v for k, v in applications.iteritems() if str(v[MUNICIPALITY_ID]) in municipalities}

    @staticmethod
    def to_applications_with_start_month(applications):
        applications_with_start_month = {}
        for application_id in applications:
            application = applications[application_id]
            month = str(application[START_TIME].month)
            applications_with_start_month[application_id] = dict(application.items() + [(MONTH, month)])
        return applications_with_start_month

    @staticmethod
    def to_applications_with_running_month(applications):
        applications_with_running_month = {}
        for application_id in applications:
            application = applications[application_id]
            month = LogEntryAnalyzer.get_running_month(application[START_TIME])
            applications_with_running_month[application_id] = dict(application.items() + [(RUNNING_MONTH, month)])
        return applications_with_running_month

    @staticmethod
    def get_running_month(start_time):
        # We wont the running month from the start of the service
        return str((start_time.year - 2013) * 12 + start_time.month)

    @staticmethod
    def filter_applications_by_operation(applications, filter_by):
        tmp = {}
        for application_id in applications:
            application = applications[application_id]
            if application[OPERATION] in filter_by:
                tmp[application_id] = application
        return tmp

    @staticmethod
    def applications_with_applications_per_month(applications):
        applications_with_per_month = {}
        with_per_month = LogEntryAnalyzer.get_application_per_month_dict(applications)
        for application_id in applications:
            application = applications[application_id]
            applications_with_per_month[application_id] = dict(application.items() + [(PER_MONTH, with_per_month[application_id])])
        return applications_with_per_month

    @staticmethod
    def get_application_per_month_dict(applications):
        grouped_by_running_month = LogEntryAnalyzer.grouped_by(applications, RUNNING_MONTH)
        with_per_month = {}
        for month, group in grouped_by_running_month:
            applications = map(lambda t: t[1], group)
            applications_per_month = len(applications)
            with_per_this_month = LogEntryAnalyzer.to_dict_with_value(applications, applications_per_month)
            with_per_month = merge_dicts(with_per_month, with_per_this_month)
        return with_per_month

    @staticmethod
    def to_dict_with_value(keys, value):
        return dict((v, value) for v in keys)

    @staticmethod
    def grouped_by(applications, target):
        sorted_by = sorted(map(lambda application_id: (applications[application_id][target], application_id), applications), key=lambda entry: entry[0])
        return groupby(sorted_by, lambda x: x[0])
