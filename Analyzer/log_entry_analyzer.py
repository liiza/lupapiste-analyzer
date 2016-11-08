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

    def get_or_create_application(self, application_id, applications, log_entry):
        if applications.has_key(application_id):
            return applications[application_id]
        else:
            application = {APPLICATION_ID: log_entry[APPLICATION_ID], MUNICIPALITY: log_entry[MUNICIPALITY]}
            if self.get_action_count:
                application[ACTION_COUNT] = 0
            if self.get_filling_time:
                application[START_TIME] = log_entry[DATE]
            applications[application_id] = application
            return application

    def to_applications(self, log_entries):
        applications = {}
        for log_entry in log_entries:

            application = self.get_or_create_application(log_entry[APPLICATION_ID], applications, log_entry)

            if log_entry[ACTION] == SUBMIT_APPLICATION and log_entry[ROLE] == APPLICANT:
                if not application.has_key(SUBMIT_APPLICATION) or application[SUBMIT_APPLICATION] > log_entry[DATE]:
                    application[SUBMIT_APPLICATION] = log_entry[DATE]

            if log_entry[ACTION] == GIVE_STATEMENT and log_entry[ROLE] == AUTHORITY:
                if not application.has_key(GIVE_STATEMENT) or application[GIVE_STATEMENT] > log_entry[DATE]:
                    application[GIVE_STATEMENT] = log_entry[DATE]

            if self.get_action_count:
                    application[ACTION_COUNT] += 1

            if self.get_filling_time:
                if not application.has_key(START_TIME) or application[START_TIME] > log_entry[DATE]:
                    application[START_TIME] = log_entry[DATE]

        return applications

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
    def to_applications_with_filling_time(applications):
        return get_time_diff_as(applications, START_TIME, SUBMIT_APPLICATION, FILLING_TIME)

    @staticmethod
    def to_applications_with_time(applications):
        return get_time_diff_as(applications, SUBMIT_APPLICATION, GIVE_STATEMENT, TIME)

    @staticmethod
    def filter_applications_with_biggest_municipalities(applications, amount):
        municipalities_and_applications_counts = LogEntryAnalyzer.get_biggest_municipalities(applications, amount)
        print "Biggest municipalities and applications " + str(municipalities_and_applications_counts)
        municipalities = map(lambda t: t[0], municipalities_and_applications_counts)
        return {k: v for k, v in applications.iteritems() if str(v[MUNICIPALITY]) in municipalities}
        # return filter(lambda id: str(applications[id][MUNICIPALITY]) in municipalities, applications)
