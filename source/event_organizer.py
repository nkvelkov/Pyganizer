import datetime
import event
import threading
from event_scheduler import EventScheduler
from file_worker import FileWorker
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow


class EventOrganizer(EventScheduler):
    def __init__(self, pending_events, active_events):
        super().__init__()
        self.file_worker = FileWorker(pending_events, active_events, passed_todos='passed_events.txt')
        self.init_id()

    def add_event(self, start_date, deadline_date, name, message):
        try:
            event = EventScheduler.add_event(start_date, deadline_date, name, message)
            self.file_worker.add_todo(event)
        except InvalidDateError:
            raise
            
    def remove_event(self, target_id):
        result = EventScheduler.remove_by_id(target_id)
        if result:
            self.file_worker.update_active_file(self.sorted_events())
        return result

    def load_saved_events(self):
        self.load_saved_active_events()
        self.load_saved_pending_events()

    def load_saved_active_events(self):
        events = self.file_worker.get_saved_active_todos()
        filtered = self.filter_passed_events(events)

        EventScheduler.add_multiple_active_events(filtered[0])

        self.file_worker.update_passed_todos(filtered[2])
        self.file_worker.update_active_file(self.sorted_events())

    def load_saved_pending_events(self):
        todos = self.file_worker.get_saved_pending_todos()
        filtered = self.filter_passed_todos(todos)

        EventScheduler.add_multiple_active_events(filtered[0])
        EventScheduler.add_multiple_pending_events(filtered[1])

        self.file_worker.update_passed_todos(filtered[2])
        self.file_worker.update_all_file(self.enumerate_todos(), self.sorted_events())

    def filter_passed_events(self, todos):
        passed_events = []
        active_events = []
        pending_events = []

        for todo in todos:
            if self.passed_date(todo.deadline_datetime):
                passed_events.append(todo)
            elif self.passed_date(todo.start_datetime):
                active_events.append(todo)
            else:
                pending_events.append(todo)
        return (active_events, pending_events, passed_events)

    def activate_pending_event(self, event):
        TaskScheduler.activate_event(event)
        self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_events())

    def expire_active_event(self, event):
        TaskScheduler.expire_active_event(event)
        self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_events())

    def handle_events(self, events):
        expired = []
        active = []

        for event in events:
            if event.mode is 'pending':
                active.append(event)
            elif event.mode is 'active':
                expired.append(event)

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

    def init_id(self):
        with open("event_id.txt", "r") as f:
            saved_id = f.readline()
            self.id = int(saved_id)

    def __del__(self):
        with open("event_id.txt", "w") as f:
            f.write("{}".format(self.id+1))