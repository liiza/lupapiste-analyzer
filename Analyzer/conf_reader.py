from cell_names import *

CONF_FILE = 'resources/conf'

class Conf:
    def __init__(self):
        self.data_file, self.params, self.filter_by, self.join_file = self.read_conf()

    def read_conf(self):
        data_file = ""
        join_file = ""
        params = ""
        filter_by = ""
        with open(CONF_FILE, 'r') as f:
            contents = self.read_file_and_skip_comments(f)
            if len(contents) < 0:
                raise ValueError("no data file name given")
            data_file, join_file = self.read_data_files(contents)
            if len(contents) > 1:
                params = contents[1]
            if len(contents) > 2:
                filter_by = contents[2].strip()
        return data_file, params, filter_by, join_file

    def read_file_and_skip_comments(self, f):
        contents = []
        for line in f:
            if line.startswith("#"):
                continue
            contents.append(line)
        return contents

    def read_data_files(self, contents):
        join_file = ""
        data_files = contents[0].split()
        data_file = data_files[0].strip()
        if len(data_files) > 1:
            join_file = data_files[1].strip()
        return data_file, join_file

    def get_params(self):
        return Params(
            self.should_get_action_count(self.params),
            self.should_get_time_to_first_statement(self.params),
            self.should_get_application_filling_time(self.params),
            len(self.should_filter_by(self.filter_by)) > 0,
            self.should_filter_by(self.filter_by),
            self.should_filter_by_municipality(self.params)
        )

    def should_get_action_count(self, params):
        global GET_ACTION_COUNT
        GET_ACTION_COUNT = params.find(ACTION_COUNT) >= 0
        if GET_ACTION_COUNT:
            print ACTION_COUNT
        return GET_ACTION_COUNT

    def should_get_time_to_first_statement(self, params):
        global GET_TIME_TO_FIRST_STATEMENT
        GET_TIME_TO_FIRST_STATEMENT = params.find(TIME) > 0
        if GET_TIME_TO_FIRST_STATEMENT:
            print TIME
        return GET_TIME_TO_FIRST_STATEMENT

    def should_get_application_filling_time(self, params):
        global GET_FILLING_TIME
        GET_FILLING_TIME = params.find(FILLING_TIME) >= 0
        if GET_FILLING_TIME:
            print FILLING_TIME
        return GET_FILLING_TIME

    def should_filter_by(self, filter_by):
        global FILTER_BY_OPERATION, FILTER_BY
        FILTER_BY_OPERATION = len(filter_by) > 0
        if FILTER_BY_OPERATION:
            FILTER_BY = filter_by
            print "filter by " + FILTER_BY
        return FILTER_BY

    def should_filter_by_municipality(self, params):
        global FILTER_BY_MUNICIPALITY
        FILTER_BY_MUNICIPALITY = params.find(MUNICIPALITY) >= 0
        if FILTER_BY_MUNICIPALITY:
            print MUNICIPALITY
        return FILTER_BY_MUNICIPALITY


class Params:
    def __init__(self, get_action_count, get_time_to_first_statement, application_filling_time, filter_by_operation, filter_by, filter_by_municipality):
        self.get_action_count = get_action_count
        self.get_time_to_first_statement = get_time_to_first_statement
        self.application_filling_time = application_filling_time
        self.filter_by_operation = filter_by_operation
        self.filter_by = filter_by
        self.filter_by_municipality = filter_by_municipality
