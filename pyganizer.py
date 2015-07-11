import datetime
import event
import threading
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow


class Pyganizer:
    def __init__(self):
        self.todos = {}  # should be read from a file
        self.active_tasks = []
        self.active_events = []
        self.termination_flag = False

    def execute(self):
        self.add_saved_moments()

        thread = threading.Thread(target=self.start_execution)
        thread.start()

    def start_execution(self):
        self.termination_flag = False

        while not self.termination_flag:
            utc = arrow.utcnow().to('local')
            current_moment = self.get_date(utc)

            if self.todos.get(current_moment) is not None:
                self.signal(current_moment)

            time.sleep(1)

    def add_saved_moments(self):
        moments = []

        with open('work_data.txt', 'r') as f:
            f.readline()
            moments = f.readlines()
            if moments is not []:
                for moment in moments:
                    if moment is not '\n' and moment is not ' ':
                        todo = moment.split(' ')
                        todo_date = (todo[1], todo[2], todo[3],
                                     todo[4], todo[5], todo[6])

                        if todo[0] == 'event':
                            self.add_event(todo_date, todo[7],
                                           todo[8], todo[9])
                        else:
                            self.add_task(todo_date, todo[7], todo[8],
                                          int(todo[9]), int(todo[10]))

    def signal(self, date):
        for todo in self.todos[date]:
            if type(todo) is Event:
                if todo.mode == 'deadline':
                    self.remove_todo(todo.alert_event)
                    self.remove_todo(todo)
                elif todo.mode == 'active':
                    self.active_events.append(todo)
            elif type(todo) is Task:
                if todo.completeness <= 0:
                    self.remove_todo(todo)
                else:
                    self.active_tasks.append(todo)

            notification_message = "{} {}\n".format(todo.name, todo.message)
            with open('passed_data.txt', 'a') as f:
                f.write(notification_message)

    def add_event(self, date, name, message, alert_seconds=0, alert_minutes=0,
                  alert_hours=1, alert_days=0, alert_months=0):
        alert_moment = self.calculate_date(
            date, alert_seconds,
            alert_hours, alert_days,
            alert_months
        )

        if not alert_moment in self.todos.keys():
            self.todos[alert_moment] = []
        alert_event = Event(alert_moment, name, message, 'active')
        alert_event.deadline_date = date
        self.todos[alert_moment].append(alert_event)
        self.write_in_file(alert_moment, alert_event)

        if not date in self.todos.keys():
            self.todos[date] = []
        target_event = Event(date, name, message, 'deadline')
        target_event.alert_event = alert_event
        self.todos[date].append(target_event)
        self.write_in_file(date, alert_event)

    def add_task(self, start_date, name, message, completeness, priority=1):
        if not start_date in self.todos.keys():
            self.todos[start_date] = []

        target_task = Task(start_date, name, message, completeness, priority)
        self.todos[start_date].append(target_task)
        self.write_in_file(start_date, target_task)

    def insert_task(self, task):
        if not task.date in self.todos.keys():
            self.todos[task.date] = []
        self.todos[task.date].append(task)
        self.write_in_file(task.date, task)

    def calculate_date(self, date, alert_seconds=0, alert_minutes=0,
                       alert_hours=0, alert_days=0, alert_months=0):
        new_day, new_month, new_year, new_hour, new_minute, new_second = date

        target_time = arrow.Arrow(new_year, new_month, new_day,
                                  new_hour, new_minute, new_second)
        alert_time = target_time.replace(
            seconds=-alert_seconds, minutes=-alert_minutes,
            hours=-alert_hours, days=-alert_days, months=-alert_months
        )

        current_moment = arrow.utcnow().to('local')

        if alert_time > current_moment:
            current_moment = current_moment.replace(seconds=+1)
            return self.get_date(current_moment)
        return self.get_date(alert_time)

    def add_task_progress(self, todo, progress):
        todo.completeness -= progress
        if todo.completeness <= 0:
            self.remove_todo(todo)

        self.update_file()

    def add_task_progress_by_name(self, date, name, progress):
        for todo in self.todos[date]:
            if todo.name == name:
                todo.completeness -= progress
                if todo.completeness <= 0:
                    self.remove_by_name(date, todo.name)

        self.update_file()

    def remove_todo(self, todo):
        key = todo.date
        self.todos[key].pop(self.todos[key].index(todo))

        if type(todo) is Task and todo in self.active_tasks:
            self.remove_active_task(todo)
        if type(todo) is Event and todo in self.active_events:
            self.remove_active_event(todo)

        keys = self.todos.keys()
        {key: self.todos[key] for key in keys if self.todos[key] != []}

        self.update_file()

    def remove_by_name(self, key, name):
        for todo in self.todos[key]:
            if todo.name == name:
                self.todos[key].pop(self.todos[key].index(todo))
                if type(todo) is Task and todo in self.active_tasks:
                    self.remove_active_task(todo)
                if type(todo) is Event and todo in self.active_events:
                    self.remove_active_event(todo)

        keys = self.todos.keys()
        {key: self.todos[key] for key in keys if self.todos[key] != []}

        self.update_file()

    def update_file(self):
        with open('work_data.txt', 'w') as f:
            f.write("{} {} {}\n".format(
                "type day month year hour minute",
                "second name message alert_hours",
                "completeness* priority*"
            ))

            for key in self.todos.keys():
                for todo in self.todos[key]:
                    f.write("{}\n".format(self.stringify(key)))

    def write_in_file(self, date, todo):
        with open("work_data", "a") as f:
            f.write("{} {}\n".format(self.stringify_date(date), str(todo)))

    def stringify(self, key):
        target_todos = self.todos[key]

        for todo in target_todos:
            if type(todo) is Task:
                return "{0} {1} {2} {3} {4} {5}".format(
                    'task', self.stringify_date(key), todo.name,
                    todo.message, todo.completeness, todo.priority
                )
            else:
                return "{0} {1} {2} {3}".format(
                    'event', self.stringify_date(key), todo.name, todo.message
                )

    def name_exists(self, date, target_name):
        if not date in self.todos.keys():
            raise DateTimeDoesNotExistsError
        return target_name in [
            name for name in map(lambda todo: todo.name, self.todos[date])
        ]

    def stringify_date(self, date):
        return "{0} {1} {2} {3} {4} {5}".format(date[0], date[1], date[2],
                                                date[3], date[4], date[5])

    def get_date(self, date):
        return (date.day, date.month, date.year,
                date.hour, date.minute, date.second)

    def terminate(self):
        self.termination_flag = True

    def remove_active_event(self, event):
        self.active_events.pop(self.active_events.index(event))

    def remove_active_task(self, task):
        self.active_tasks.pop(self.active_tasks.index(task))

    def get_todo(self, date, todo_name):
        for todo in self.todos[date]:
            if todo.name == todo_name:
                return todo
        return None
