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
            {ACTION_COUNT: self.should_get_action_count(self.params),
             TIME_TO_STATEMENT: self.should_get_time_to_first_statement(self.params),
             FILLING_TIME: self.should_get_application_filling_time(self.params),
             "filter": len(self.filter_by_operation(self.filter_by)) > 0,
             "filter_by": self.filter_by_operation(self.filter_by),
             MUNICIPALITY: self.should_filter_by_municipality(self.params),
             "log": self.should_use_logarithmic_numbers(self.params),
             MONTH: self.should_add_start_month(self.params),
             TIME_TO_VERDICT: self.should_get_time_to_verdict(self.params)}
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
    def filter_by_operation(fltr_by):
        fltr_by_operation = len(fltr_by) > 0
        filter_by = []
        if fltr_by_operation:
            filter_by = fltr_by.split()
            print "filter by " + str(filter_by)
        return filter_by

    @staticmethod
    def should_filter_by_municipality(params):
        filter_by_municipality = params.find(MUNICIPALITY) >= 0
        if filter_by_municipality:
            print "filter by biggest municipalities"
        return filter_by_municipality

    @staticmethod
    def should_use_logarithmic_numbers(params):
        use_log = params.find("log") >= 0
        if use_log:
            print "using logaritmic numbers"
        return use_log

    @staticmethod
    def should_add_start_month(params):
        use_month = params.find(MONTH) >= 0
        if use_month:
            print "add start month"
        return use_month

    def should_get_time_to_verdict(self, params):
        time_to_verdict = params.find(TIME_TO_VERDICT) >= 0
        if time_to_verdict:
            print "add time to verdict"
        return time_to_verdict




class Params:
    def __init__(self, params):
        self.get_action_count = params[ACTION_COUNT]
        self.get_time_to_first_statement = params[TIME_TO_STATEMENT]
        self.application_filling_time = params[FILLING_TIME]
        self.filter_by_operation = params["filter"]
        self.filter_by = params["filter_by"]
        self.filter_by_municipality = params[MUNICIPALITY]
        self.logarithmic_numbers = params["log"]
        self.month = params[MONTH]
        self.time_to_verdict = params[TIME_TO_VERDICT]
