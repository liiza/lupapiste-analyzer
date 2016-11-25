import unittest

from log_entry_analyzer import *


class TestLogEntryAnalyzer(unittest.TestCase):
    def test_should_return_applications_per_month(self):
        applications = {"1": {RUNNING_MONTH: 1, APPLICATION_ID: "1"},
                        "2": {RUNNING_MONTH: 1, APPLICATION_ID: "2"},
                        "3": {RUNNING_MONTH: 2, APPLICATION_ID: "3"}}

        application_with_per_month = LogEntryAnalyzer.applications_with_applications_per_month(applications)

        self.assertEqual(application_with_per_month["1"][PER_MONTH], 2)
        self.assertEqual(application_with_per_month["2"][PER_MONTH], 2)
        self.assertEqual(application_with_per_month["3"][PER_MONTH], 1)

    def test_should_return_dict_with_value(self):
        dict = LogEntryAnalyzer.to_dict_with_value(["1", "2", "3"], "value")

        self.assertEqual(dict["1"], "value")
        self.assertEqual(dict["2"], "value")
        self.assertEqual(dict["3"], "value")


if __name__ == '__main__':
    unittest.main()
