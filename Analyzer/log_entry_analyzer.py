from cell_names import *
from data_helpers import *


class LogEntryAnalyzer:
    def __init__(self, get_action_count, get_filling_time, filter_by_operation, filter_by):
        self.get_action_count = get_action_count
        self.get_filling_time = get_filling_time
        self.filter_by_operation = filter_by_operation
        self.filter_by = filter_by

    def get_or_create_application(self, application_id, applications, log_entry):
        if applications.has_key(application_id):
            return applications[application_id]
        else:
            application = {MUNICIPALITY: log_entry[MUNICIPALITY]}
            if self.get_action_count:
                application[ACTION_COUNT] = 0
            if self.get_filling_time:
                application[START_TIME] = log_entry[DATE]
            applications[application_id] = application
            return application

    def to_applications(self, log_entries):
        applications = {}
        for log_entry in log_entries:
            if self.filter_by_operation and log_entry[OPERATION] != self.filter_by:
                continue

            application = self.get_or_create_application(log_entry[APPLICATION_ID], applications, log_entry)

            if log_entry[ACTION] == SUBMIT_APPLICATION and log_entry[ROLE] == APPLICANT:
                if not application.has_key(SUBMIT_APPLICATION) or application[SUBMIT_APPLICATION] > log_entry[DATE]:
                    application[SUBMIT_APPLICATION] = log_entry[DATE]

            elif log_entry[ACTION] == GIVE_STATEMENT and log_entry[ROLE] == AUTHORITY:
                if not application.has_key(GIVE_STATEMENT) or application[GIVE_STATEMENT] > log_entry[DATE]:
                    application[GIVE_STATEMENT] = log_entry[DATE]

            elif self.get_action_count:
                application[ACTION_COUNT] += 1

            if self.get_filling_time:
                if not application.has_key(START_TIME) or application[START_TIME] > log_entry[DATE]:
                    application[START_TIME] = log_entry[DATE]

        return applications

    def to_applications_with_filling_time(self, applications):
        return diff(applications, START_TIME, SUBMIT_APPLICATION, FILLING_TIME)

    def to_applications_with_time(self, applications):
        return diff(applications, SUBMIT_APPLICATION, GIVE_STATEMENT, TIME)
