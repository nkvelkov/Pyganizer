import arrow

class Event:
    def __init__(self, datetime, name, message, mode, eid):
        self.date = datetime
        self.name = name
        self.message = message
        self.mode = mode
        self.eid = eid

    def __str__(self):
        return "{} {} {}".format(self.date_to_string(), self.name, self.message)

    def to_string(self):
        return "{} {}".format(str(self.date), self.name)

    def date_to_string(self):
        return "{0} {1} {2} {3} {4} {5}".format(
            self.date[0], self.date[1], self.date[2],
            self.date[3], self.date[4], self.date[5]
        )