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
        self.active_todos = self.active_events

    def add_event(self, start_date, deadline_date, name, message, timezone):
        if (self.passed_date(deadline_date)
           or start_date.to('utc') >= deadline_date.to('utc')):
                raise InvalidDateError

        if self.passed_date(start_date):
            raise InvalidDateError

        mode = 'pending'
        event = Event(start_date, deadline_date, name,
                      message, mode,
                      self.get_id(), timezone)
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
            todo = self.find_active_event(event.eid)
            if todo is None:
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
        if event in self.active_events:
            self.active_events.pop(self.active_events.index(event))

    def remove_empty_entries(self):
        keys = self.todos.keys()
        self.todos = {
            key: self.todos[key] for key in keys if self.todos[key] != []
        }

    def enumerate_todos(self):
        result = []
        for holder in self.todos.values():
            for todo in holder:
                if todo.mode is 'pending':
                    result.append(todo)
        return result

    def passed_date(self, target_date):
        current_moment = arrow.now()
        return target_date.to('utc') < current_moment.to('utc')

    def find_pending_event(self, tid):
        for key in self.todos.keys():
            for todo in self.todos[key]:
                if todo.tid == tid:
                    return todo
        return None

    def get_todo(self, date, todo_name):
        for todo in self.todos[date]:
            if todo.name == todo_name:
                return todo
        return None
