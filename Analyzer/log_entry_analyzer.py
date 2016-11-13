import operator
from itertools import groupby

from data_helpers import *


class LogEntryAnalyzer:
    def __init__(self, get_time_to_first_statement=False, get_action_count=False, get_filling_time=False, filter_by_operation=False, filter_by=None):
        self.get_time_to_first_statement = get_time_to_first_statement
        self.get_action_count = get_action_count
        self.get_filling_time = get_filling_time
        self.filter_by_operation = filter_by_operation
        self.filter_by = filter_by

    def to_applications(self, log_entries):
        applications = {}
        for log_entry in log_entries:
            application = self.get_or_create_application(log_entry[APPLICATION_ID], applications, log_entry)

            if self.get_filling_time:
                if START_TIME not in application or application[START_TIME] > log_entry[DATE]:
                    application[START_TIME] = log_entry[DATE]

            if log_entry[ACTION] == SUBMIT_APPLICATION and log_entry[ROLE] == APPLICANT:
                if SUBMIT_APPLICATION not in application or application[SUBMIT_APPLICATION] < log_entry[DATE]:
                    application[SUBMIT_APPLICATION] = log_entry[DATE]

            if log_entry[ACTION] == GIVE_STATEMENT and log_entry[ROLE] == AUTHORITY:
                if GIVE_STATEMENT not in application or application[GIVE_STATEMENT] > log_entry[DATE]:
                    application[GIVE_STATEMENT] = log_entry[DATE]

            if self.get_action_count and log_entry[ROLE] == APPLICANT:
                if ACTION_COUNT not in application:
                    application[ACTION_COUNT] = 0
                application[ACTION_COUNT] += 1


        return applications

    @staticmethod
    def get_or_create_application(application_id, applications, log_entry):
        if application_id in applications:
            return applications[application_id]
        else:
            application = {APPLICATION_ID: log_entry[APPLICATION_ID], MUNICIPALITY: log_entry[MUNICIPALITY]}
            applications[application_id] = application
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
        return lambda application_id: (applications[application_id][MUNICIPALITY], applications[application_id])

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
        return {k: v for k, v in applications.iteritems() if str(v[MUNICIPALITY]) in municipalities}

    def to_applications_with_start_month(self, applications):
        applications_with_start_month = {}
        for application_id in applications:
            application = applications[application_id]
            month = application[START_TIME].month
            applications_with_start_month[application_id] = dict(application.items() + [(MONTH, month)])
        return applications_with_start_month
