import event


class Task(Event):
    def __init__(self, datetime, name, completeness):
        self.datetime = datetime
        self.name = name
        self.completeness = completeness
