from event import Event
import json


class Task(Event):
    def __init__(self, datetime, name, message, completeness, priority, tid):
        self.datetime = datetime
        self.name = name
        self.message = message
        self.completeness = completeness
        self.priority = priority
        self.tid = tid

    def add_progress(self, completeness):
        self.completeness -= completeness
 
    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.datetime, self.name, self.message, self.completeness, self.priority)
    
    def foo(self):
        return "{0} {1} {2} {3} {4}".format(
            self.date_to_string(), self.name, self.message,
            str(self.completeness), str(self.priority)
        )
