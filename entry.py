from peewee import *

import datetime


db = SqliteDatabase('entries.db')


class Entry(Model):
    """
    Entry database model that stores the employee's name, time worked, task
    worked on, and general notes about the task.
    """
    employee_name = CharField(max_length=55)
    minutes = IntegerField()
    task_name = CharField(max_length=55)
    notes = TextField(null=True)
    date = DateTimeField(default=datetime.datetime.now)


    # Tell the model which database to connect to
    class Meta:
        database = db


def initialize():
    """Create the database and the tables if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)
