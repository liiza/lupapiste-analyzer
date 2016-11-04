DATE = 'date'
USER_ID = 'userId'
ROLE = 'role'
MUNICIPALITY = 'municipality'
APPLICATION_ID = 'applicationId'
ACTION = 'action'
TARGET = 'target'
IS_INFO_REQUEST = "isInfoRequest"
OPERATION = "operation"
SUBMIT_APPLICATION = 'submit-application'
GIVE_STATEMENT = 'give-statement'
APPLICANT = 'applicant'
AUTHORITY = 'authority'
START_TIME = 'start-time'
ACTION_COUNT = 'action-count'
TIME = 'time'
FILLING_TIME = 'filling-time'
PERMIT_TYPE = "permitType"
VERDICT_GIVEN = "verdictGivenDate"
SUBMITTED_DATE = "submittedDate" # Sopernovus
STATE = "state"

date_columns = [DATE, SUBMITTED_DATE, VERDICT_GIVEN]


def is_date(column):
    return column in date_columns


TIME_TO_VERDICT = "timeToVerdict"