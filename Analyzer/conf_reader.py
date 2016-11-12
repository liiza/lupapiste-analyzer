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

    @staticmethod
    def should_get_action_count(params):
        get_action_count = params.find(ACTION_COUNT) >= 0
        if get_action_count:
            print ACTION_COUNT
        return get_action_count

    @staticmethod
    def should_get_time_to_first_statement(params):
        get_time_to_first_statement = params.find(TIME_TO_STATEMENT) > 0
        if get_time_to_first_statement:
            print TIME_TO_STATEMENT
        return get_time_to_first_statement

    @staticmethod
    def should_get_application_filling_time(params):
        get_filling_time = params.find(FILLING_TIME) >= 0
        if get_filling_time:
            print FILLING_TIME
        return get_filling_time

    @staticmethod
    def should_filter_by(fltr_by):
        filter_by_operation = len(fltr_by) > 0
        filter_by = ""
        if filter_by_operation:
            filter_by = fltr_by
            print "filter by " + filter_by
        return filter_by

    @staticmethod
    def should_filter_by_municipality(params):
        filter_by_municipality = params.find(MUNICIPALITY) >= 0
        if filter_by_municipality:
            print MUNICIPALITY
        return filter_by_municipality


class Params:
    def __init__(self, get_action_count, get_time_to_first_statement, application_filling_time, filter_by_operation, filter_by, filter_by_municipality):
        self.get_action_count = get_action_count
        self.get_time_to_first_statement = get_time_to_first_statement
        self.application_filling_time = application_filling_time
        self.filter_by_operation = filter_by_operation
        self.filter_by = filter_by
        self.filter_by_municipality = filter_by_municipality
