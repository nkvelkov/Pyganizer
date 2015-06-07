import datetime
import time


class Pyganizer:
    def __init__(self):
        self.todos = {}  # should be read from a file

    def execute(self):
        while True:
            now = datetime.datetime.now()
            current_moment = (now.day, now.month, now.year)

            if self.tasks.get(current_moment) is not None:
                signal(self.todos[current_moment])

            time.sleep(1)

    def signal(self, message):
        print("{} {}".format(message[0], message[1]))

    def add_event(self, date, name, message, alert_hours=1):
        if alert_hours > 24:
            target_moment = calculate_date(date, alert_hours)
            self.todos[target_moment] = (name, message)
        else:
            target_moment = get_date(date)
            self.todos[target_moment] = (name, message)

    def calculate_date(self, date, alert_hours):
        pass

    def add_task(self, date, hour, name, completeness, alert_hours=1):
        if alert_hours > 24:
            target_moment = calculate_date(date, alert_hours)
            self.todos[target_moment] = (name, message, completeness)
        else:
            target_moment = get_date(date)
            self.todos[target_moment] = (name, message, completeness)

    def remove_event(self, name):
        keys = todos.keys()
        for key in keys:
            if todos[key][0] is name:
                todos.pop(key)

    def remove_task(self, name):
        keys = todos.keys()
        for key in keys:
            if todos[key][0] is name:
                todos.pop(key)

    def get_date(self, date):
        return (date.day, date.month, date.year,
                date.hour, date.minute, date.second)
