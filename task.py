from event import Event


class Task(Event):
    def __init__(self, datetime, name, message, completeness, priority):
        self.date = datetime
        self.name = name
        self.message = message
        self.completeness = completeness
        self.priority = priority
