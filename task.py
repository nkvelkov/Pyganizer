from event import Event


class Task(Event):
    def __init__(self, datetime, name, message, completeness, priority):
        self.date = datetime
        self.name = name
        self.message = message
        self.completeness = completeness
        self.priority = priority

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(
            self.date_to_string(), self.name, self.message,
            str(self.completeness), str(self.priority)
        )
