import unittest
import unittest.mock as mock

from playhouse.test_utils import test_database
from peewee import *
from datetime import datetime

import worklog
from entry import Entry


TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([Entry], safe=True)

DATA = {
    "employee_name": "Brian Weber",
    "minutes": 120,
    "task_name": "Surfing",
    "notes": "These are my notes.",
    "date": "12/25/2016"
    }


class WorkLogTests(unittest.TestCase):
    @staticmethod
    def create_entries():
        Entry.create(
            employee_name=DATA["employee_name"],
            minutes=DATA["minutes"],
            task_name=DATA["task_name"],
            notes=DATA["notes"],
            date=DATA["date"]
        )


    def test_get_employee_name(self):
        with mock.patch('builtins.input',
            return_value=DATA["employee_name"]):
            assert worklog.get_employee_name() == DATA["employee_name"]


    def test_get_task_name(self):
        with mock.patch('builtins.input',
            return_value=DATA["task_name"]):
            assert worklog.get_task_name() == DATA["task_name"]


    def test_get_time_spent(self):
        with mock.patch('builtins.input',
            return_value=DATA["minutes"]):
            assert worklog.get_time_spent() == DATA["minutes"]


    def test_time_spent_not_int(self):
        with mock.patch('builtins.input', return_value="number"):
            self.assertRaises(ValueError)


    def test_get_notes(self):
        with mock.patch('builtins.input',
            return_value=DATA["notes"]):
            assert worklog.get_notes() == DATA["notes"]


    def test_get_date(self):
        with mock.patch('builtins.input',
            return_value=DATA["date"]):
            assert worklog.get_date() == DATA["date"]


    def test_add_entry(self):
        with mock.patch('builtins.input',
            side_effect=["12/25/2016", "Name", "Surfing", 45,
            "Hang ten dude!", "y", ""]
            , return_value=DATA):
            assert worklog.add_entry()["task_name"] == DATA["task_name"]


    def test_search_entries(self):
        with test_database(TEST_DB, (Entry,)):
            self.create_entries()
            with mock.patch('builtins.input',
                side_effect=["e", "Brian Weber", "q"]):
                assert worklog.search_entries().count() == 1

            with mock.patch('builtins.input',
                side_effect=["d", "12/25/2016", "q"]):
                assert worklog.search_entries().count() == 1

            with mock.patch('builtins.input',
                side_effect=["r", "12/01/2016", "12/31/2016", "q"]):
                assert worklog.search_entries().count() == 1

            with mock.patch('builtins.input',
                side_effect=["k", "Surfing", "q"]):
                assert worklog.search_entries().count() == 1


    def test_edit_entry(self):
        with test_database(TEST_DB, (Entry,)):
            self.create_entries()


    def test_delete_entry(self):
        pass


if __name__ == '__main__':
    unittest.main()
