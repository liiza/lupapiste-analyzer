from data_helpers import *

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


class LogEntryAnalyzer:
    def __init__(self, get_action_count, get_filling_time, filter_by_operation):
        self.get_action_count = get_action_count
        self.get_filling_time = get_filling_time
        self.filter_by_operation = filter_by_operation

    def to_cells(self, line):
        chunks = line.split(";")
        return {DATE: to_date(chunks[COLUMNS.index(DATE)]),
                ROLE: chunks[COLUMNS.index(ROLE)],
                MUNICIPALITY: chunks[COLUMNS.index(MUNICIPALITY)],
                APPLICATION_ID: chunks[COLUMNS.index(APPLICATION_ID)],
                ACTION: chunks[COLUMNS.index(ACTION)],
                OPERATION: chunks[COLUMNS.index(OPERATION)]}

    def to_log_entries(self, data):
        header = True
        data_entries = []
        for line in data:
            if header:
                header = False
                continue
            data_entries.append(self.to_cells(line))
        return data_entries

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
            if self.filter_by_operation and log_entry[OPERATION] != 'pientalo':
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
