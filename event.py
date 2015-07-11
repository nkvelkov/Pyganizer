import arrow

class Event:
    def __init__(self, datetime, name, message, mode):
        self.date = datetime
        self.name = name
        self.message = message
        self.mode = mode

    def __str__(self):
        return "{} {}".format(self.name, self.message)

    def to_string(self):
        return "{} {}".format(str(self.date), self.name)