import datetime
import event
import threading
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow


class Scheduler:
    def __init__(self):
        self.todos = {}  # should be read from a file
        self.active_tasks = []
        self.active_events = []

    def add_event(self, date, name, message, alert_seconds=0, alert_minutes=0,
                  alert_hours=1, alert_days=0, alert_months=0):
        # date = self.get_date_tuple(date)
        alert_moment = self.calculate_date(
            date, alert_seconds,
            alert_hours, alert_days,
            alert_months
        )

        if not alert_moment in self.todos.keys():
            self.todos[alert_moment] = []
            print("ij")
        alert_event = Event(alert_moment, name, message, 'active')
        alert_event.deadline_date = date
        self.todos[alert_moment].append(alert_event)
        print('asdf')
        print(self.todos)
        if not date in self.todos.keys():
            self.todos[date] = []
        target_event = Event(date, name, message, 'deadline')
        target_event.alert_event = alert_event
        self.todos[date].append(target_event)
        print(self.todos)

    def add_task(self, start_date, name, message, completeness, priority=1):
        if not start_date in self.todos.keys():
            self.todos[start_date] = []

        target_task = Task(start_date, name, message, completeness, priority)
        self.todos[start_date].append(target_task)

    def insert_task(self, task):
        if not task.date in self.todos.keys():
            self.todos[task.date] = []
        self.todos[task.date].append(task)

    def calculate_date(self, date, alert_seconds=0, alert_minutes=0,
                       alert_hours=0, alert_days=0, alert_months=0):
        # new_day, new_month, new_year, new_hour, new_minute, new_second = date
        # target_time = arrow.Arrow(new_year, new_month, new_day,
        #                        new_hour, new_minute, new_second)
        alert_time = date.replace(
            seconds=-alert_seconds, minutes=-alert_minutes,
            hours=-alert_hours, days=-alert_days, months=-alert_months
        )

        current_moment = arrow.utcnow().to('local')
        # print("cur{} alert{}".format(self.get_date(current_moment), self.get_date(alert_time)))

        if alert_time < current_moment:
          #  print("AdsfADS")
            current_moment = current_moment.replace(seconds=+1)
            return self.get_date_tuple(current_moment)
        # print("ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖжж")
        return self.get_date_tuple(alert_time)

    def add_task_progress(self, todo, progress):
        todo.completeness -= progress
        if todo.completeness <= 0:
            self.remove_todo(todo)

    def add_task_progress_by_name(self, date, name, progress):
        for todo in self.todos[date]:
            if todo.name == name:
                todo.completeness -= progress
                if todo.completeness <= 0:
                    self.remove_by_name(date, todo.name)

    def remove_todo(self, todo):
        key = todo.date
        self.todos[key].pop(self.todos[key].index(todo))

        if type(todo) is Task and todo in self.active_tasks:
            self.remove_active_task(todo)
        if type(todo) is Event and todo in self.active_events:
            self.remove_active_event(todo)

        keys = self.todos.keys()
        {key: self.todos[key] for key in keys if self.todos[key] != []}


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

    def get_date_tuple(self, date):
        if type(date) is tuple:
            return date
        else:
            return (date.day, date.month, date.year,
                    date.hour, date.minute, date.second)

    def get_date(self, date):
        if type(date) is tuple:
            return date
        else:
            return (date.day, date.month, date.year,
                    date.hour, date.minute, date.second)

    def remove_active_event(self, event):
        self.active_events.pop(self.active_events.index(event))

    def remove_active_task(self, task):
        self.active_tasks.pop(self.active_tasks.index(task))

    def get_todo(self, date, todo_name):
        for todo in self.todos[date]:
            if todo.name == todo_name:
                return todo
        return None

# todo: to create a new class inheriting arrow in order to make its objects hashable