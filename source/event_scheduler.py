import datetime
import event
import threading
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow
from my_exceptions import *


class EventScheduler:
    def __init__(self):
        self.todos = {}  # should be read from a file
        self.active_events = []

    def add_event(self, start_date, deadline_date, name, message, timezone):
        if self.passed_date(deadline_date) or start_date.to('utc') > deadline_date.to('utc'):
            raise InvalidDateError

        if self.passed_date(start_date):
            start_date = arrow.now()
            timezone = 'local'

        event = Event(start_date, deadline_date, name,
                      message, 'pending', self.get_id(), timezone)

        self.queue_event(event)

        return event

    def queue_event(self, event):
        alert_moment = event.start_datetime
        target_moment = event.deadline_datetime

        self.add_event_by_date(alert_moment, event)
        self.add_event_by_date(target_moment, event)

    def add_event_by_date(self, date, event):
        if not date in self.todos.keys():
            self.todos[date] = []
        self.todos[date].append(event)

    def add_multiple_active_events(self, events):
        new = []
        for event in events:
            event.mode = 'active'
            new.append(event)
            self.add_event_by_date(event.deadline_datetime, event)
        self.active_events.extend(new)

    def add_multiple_pending_events(self, events):
        for event in events:
            event.mode = 'pending'
            self.add_event_by_date(event.start_datetime, event)
            self.add_event_by_date(event.deadline_datetime, event)

    def activate_event(self, event):
        self.remove_event_with_key(event, event.start_datetime)
        event.mode = 'active'
        self.active_events.append(event)

    def expire_active_event(self, event):
        self.remove_event_with_key(event, event.deadline_datetime)
        self.remove_active_event(event)

    def find_active_event(self, target_id):
        for todo in self.active_events:
            if todo.eid == target_id:
                return todo
        return None

    def remove_event_with_key(self, event, key):
        if key in self.todos.keys():
            if event in self.todos[key]:
                self.todos[key].pop(self.todos[key].index(event))
                self.remove_empty_entries()

    def remove_by_id(self, target_id):
        event = self.find_active_event(target_id)
        if event is not None:
            self.remove_todo(event)
            return True
        return False

    def remove_todo(self, todo):
        start_key = todo.start_datetime
        end_key = todo.deadline_datetime

        if todo in self.active_events:
           self.remove_active_event(todo)

        if start_key in self.todos.keys():
            if todo in self.todos[start_key]:
                self.todos[start_key].pop(self.todos[start_key].index(todo))
        
        if end_key in self.todos.keys():
            if todo in self.todos[end_key]:
                self.todos[end_key].pop(self.todos[end_key].index(todo))

        self.remove_empty_entries()

    def remove_empty_entries(self):
        keys = self.todos.keys()
        {key: self.todos[key] for key in keys if self.todos[key] != []}

    def passed_date(self, target_date):
        current_moment = arrow.now()
        print(current_moment)
        print(target_date)
        print(target_date.to('utc') < current_moment.to('utc'))
        return target_date.to('utc') < current_moment.to('utc')

    def get_id(self):
        result_id = 1  
        with open("work_files/event_id.txt", "r") as f:
            saved_id = f.readline()
            if saved_id.isnumeric():
                result_id = int(saved_id) + 1

        with open("work_files/event_id.txt", "w") as f:
            f.write(str(result_id))

        return result_id

    def remove_active_event(self, event):
        self.active_events.pop(self.active_events.index(event))

    def enumerate_todos(self):
        result = set()
        for holder in self.todos.values():
            for todo in holder:
                result.add(todo)
        return result

    def find_pending_event(self, tid):
        for key in self.todos.keys():
            for todo in self.todos[key]:
                if todo.tid == tid:
                    return todo
        return None

    def calculate_date(self, date, alert_seconds=0, alert_minutes=0,
                       alert_hours=0, alert_days=0, alert_months=0):
        alert_time = date.replace(
            seconds=-alert_seconds, minutes=-alert_minutes,
            hours=-alert_hours, days=-alert_days, months=-alert_months
        )

        current_moment = arrow.utcnow().to('local')

        if alert_time < current_moment:
            current_moment = current_moment.replace(seconds=+1)
            return self.get_date_tuple(current_moment)
        return self.get_date_tuple(alert_time)

    def add_event_with_date_offset(self, date, name, message, alert_seconds=0, alert_minutes=0,
                  alert_hours=1, alert_days=0, alert_months=0):
        # date = self.get_date_tuple(date)
        a = arrow.utcnow().to('local')
        alert_moment = self.calculate_date(
            date, alert_seconds,
            alert_hours, alert_days,
            alert_months
        )

        alert_event = Event(alert_moment, name, message, 'active', self.get_id())
        target_event = Event(date, name, message, 'deadline', self.get_id())

        self.add_chained_events(alert_event, target_event)

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

    def get_todo(self, date, todo_name):
        for todo in self.todos[date]:
            if todo.name == todo_name:
                return todo
        return None

    def remove_by_name(self, key, name):
        for todo in self.todos[key]:
            if todo.name == name:
                remove_todo(todo)
                return True
        return False
        