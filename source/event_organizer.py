import datetime
import event
import threading
from event_scheduler import EventScheduler
from file_worker import FileWorker
from event import Event
from task import Task
import time
import calendar
import arrow
from my_exceptions import *
import icalendar
from icalendar import Calendar


class EventOrganizer(EventScheduler):
    def __init__(self, pending_events, active_events, ical_file):
        super().__init__()
        self.file_worker = FileWorker(pending_events, active_events, ical_file, passed_todos='work_files/passed_events.txt')
        self.ical_file = ical_file

    def add_event(self, start_date, deadline_date, name, message, timezone='local'):
        try:
            event = EventScheduler.add_event(self, start_date, deadline_date, name, message, timezone)
            self.file_worker.add_todo(event)
        except InvalidDateError:
            raise
            
    def remove_event(self, target_id):
        result = EventScheduler.remove_by_id(self, target_id)
        print(result)
        if result:
            self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_events())
        return result

    def load_saved_events(self):
        self.load_saved_active_events()
        self.load_saved_pending_events()

    def load_saved_active_events(self):
        events = self.file_worker.get_saved_active_todos()
        filtered = self.filter_passed_events(events)

        EventScheduler.add_multiple_active_events(self, filtered[0])

        self.file_worker.update_passed_todos(filtered[2])
        self.file_worker.update_active_file(self.sorted_events())

    def load_saved_pending_events(self):
        todos = self.file_worker.get_saved_pending_todos()
        filtered = self.filter_passed_events(todos)

        EventScheduler.add_multiple_active_events(self, filtered[0])
        EventScheduler.add_multiple_pending_events(self, filtered[1])

        self.file_worker.update_passed_todos(filtered[2])
        self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_events())

    def filter_passed_events(self, todos):
        passed_events = set()
        active_events = set()
        pending_events = set()

        for todo in todos:
            if self.passed_date(todo.deadline_datetime):
                passed_events.add(todo)
            elif self.passed_date(todo.start_datetime):
                active_events.add(todo)
            else:
                pending_events.add(todo)
        return (active_events, pending_events, passed_events)

    def activate_pending_event(self, event):
        EventScheduler.activate_event(self, event)
        self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_events())

    def expire_active_event(self, event):
        EventScheduler.expire_active_event(self, event)
        self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_events())

    def handle_events(self, events):
        expired = []
        active = []

        for event in events:
            if event.mode is 'pending':
                active.append(event)
            elif event.mode is 'active':
                expired.append(event)

        print(active)
        print(expired)
        self.activate_pending_events(active)
        self.expire_active_events(expired)

    def activate_pending_events(self, events):
        for event in events:
            self.activate_pending_event(event)

    def expire_active_events(self, events):
        for event in events:
            self.expire_active_event(event)

    def sorted_events(self):
        return sorted(self.active_events, key=lambda e: e.deadline_datetime)

    def export_ical(self):
        self.file_worker.update_ical_file(self.active_events)

    def has_moment(self, moment):
        for key in self.todos.keys():
            if key.to('utc') < moment.to('utc') or key.to('utc') is moment.to('utc'):
                return True
        return False

    def handle_moment(self, moment):
        for key in self.todos.keys():
            if key.to('utc') < moment.to('utc'):
                print("in handle_moment")
                self.handle_events(self.todos[key])


