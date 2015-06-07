import datetime


class Event:
    def __init__(self, datetime, name):
        self.datetime = datetime
        self.name = name


class Task(Event):
    def __init__(self, datetime, name, completeness):
        self.datetime = datetime
        self.name = name
        self.completeness = completeness


class Pyganizer:
    def __init__(self):
        self.tasks = {}  # should be read from a file

    def execute(self):

        while True:
            current_time = datetime.datetime.now()

    def signal(self):
        pass

    def add_event(self, date, hour, name, alert_hours=1):
        pass

    def add_task(self, date, hour, name, alert_hours=1):
        pass

    def remove_event(self, date, hour, name=""):
        pass

    def remove_task(self, date, hour, name=""):
        pass
