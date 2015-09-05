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
        self.id = 0;

    def add_event(self, date, name, message, alert_seconds=0, alert_minutes=0,
                  alert_hours=1, alert_days=0, alert_months=0):
        # date = self.get_date_tuple(date)
        arrow = arrow.utcnow().to('local')
        alert_moment = self.calculate_date(
            date, alert_seconds,
            alert_hours, alert_days,
            alert_months
        )

        alert_event = Event(alert_moment, name, message, 'active')
        target_event = Event(date, name, message, 'deadline')

        self.add_chained_events(alert_event, target_event)

    def add_event(self, deadline_date, start_date, name, message):
        if passed_date(start_date):
            return False

        alert_event = Event(start_date, name, message, 'active')
        target_event = Event(deadline_date, name, message, 'deadline')

        self.add_chained_events(alert_event, target_event)

        return True

    def add_chained_events(self, alert_event, target_event):
        if not alert_moment in self.todos.keys():
            self.todos[alert_moment] = []
        alert_event.deadline_date = deadline_date
        alert_event.chain_event = target_event
        alert_event.id = self.get_id()
        self.todos[alert_moment].append(alert_event)

        if not date in self.todos.keys():
            self.todos[date] = []
        target_event.deadline_date = None
        target_event.chain_event = alert_event
        target_event.id = self.get_id()
        self.todos[date].append(target_event)

    def passed_date(self, target_date):
        current_moment = arrow.utcnow().to('local')

        return target_date < current_moment

    def add_task(self, start_date, name, message, completeness, priority=1):
        if passed_date(start_date):
            return False

        if not start_date in self.todos.keys():
            self.todos[start_date] = []

        target_task = Task(start_date, name, message, completeness, priority)
        target_task.id = self.get_id()
        self.todos[start_date].append(target_task)
        return True

    def insert_task(self, task):
        if not task.date in self.todos.keys():
            self.todos[task.date] = []
        task.id = self.get_id()
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
                self.add_task_progress(todo, progress)
    
    def add_task_progress_by_id(self, target_id, progress):
        for key in self.todos.keys():
            for todo in self.todos[key]:
                if todo.id == target_id:
                    add_task_progress(todo, progress)

    def remove_todo(self, todo):
        key = todo.date

        if type(todo) is Task:
            self.todos[key].pop(self.todos[key].index(todo))
            if todo in self.active_tasks:
                self.remove_active_task(todo)

        if type(todo) is Event:
            chain_event = todo.chain_event
            chain_key = chain_event.date
            self.todos[chain_key].pop(self.todo[chain_key].index(chain_event))
            self.todos[key].pop(self.todos[key].index(todo))

            if todo in self.active_events:
                self.remove_active_event(todo)

            if chain_event in self.active_events:
                self.remove_active_event(chain_event)

        self.remove_empty_entries()

    def remove_by_name(self, key, name):
        for todo in self.todos[key]:
            if todo.name == name:
                remove_todo(todo)
                return True
        return False

    def remove_by_id(self, target_id):
        for key in self.todos.keys():
            for todo in self.todos[key]:
                if todo.id == target_id:
                    remove_todo(todo)
                    return True
        return False

    def remove_empty_entries(self):
        keys = self.todos.keys()
        {key: self.todos[key] for key in keys if self.todos[key] != []}

    def get_id(self):
        self.id = self.id + 1
        return self.id

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

    def activate_task(self, task):
        if not self_has_todo(task):
            pass
        self.activate_task.append(task)

    def activate_event(self, event):
        if not self_has_todo(event):
            pass
        self.activate_event.append(event)
        
# todo to make a new class to work with the files, file_worker
# todo: to create a new class inheriting arrow in order to make its objects hashable