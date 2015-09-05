import datetime
import event
import threading
from task_scheduler import TaskScheduler
from file_worker import FileWorker
from event import Event
from task import Task
import time
import calendar
import arrow
import icalendar
from icalendar import Calendar

class TaskOrganizer(TaskScheduler):
    def __init__(self, pending_tasks_file, active_tasks_file, ical_file):
        super().__init__()
        self.file_worker = FileWorker(pending_tasks_file, active_tasks_file, ical_file)
        self.ical_file = ical_file

    def add_task(self, start_date, name, message, completeness, priority=1, timezone='local'):
        task = self.append_task(start_date, name, message, completeness, priority, timezone)
        self.file_worker.add_todo(task)

    def add_task_progress(self, target_id, progress):
        result = TaskScheduler.add_task_progress_by_id(self, target_id, progress) # to implement proper exception handling
        if result:
            self.file_worker.update_active_file(self.sorted_tasks())
        return result

    def set_task_priority(self, target_id, priority):
        result = TaskScheduler.add_task_priority_by_id(self, target_id, priority) # to implement proper exception handling
        if result:
            self.file_worker.update_active_file(self.sorted_tasks())
        return result

    def remove_task(self, target_id):
        result = TaskScheduler.remove_by_id(self, target_id)
        if result:
            self.file_worker.update_active_file(self.sorted_tasks())
        return result

    def load_saved_tasks(self):
        self.load_saved_active_tasks()
        self.load_saved_pending_tasks()

    def load_saved_active_tasks(self):
        tasks = self.file_worker.get_saved_active_todos()
        TaskScheduler.add_multiple_active_tasks(self, tasks)

    def load_saved_pending_tasks(self):
        todos = self.file_worker.get_saved_pending_todos()

        filtered = self.filter_passed_tasks(todos)

        TaskScheduler.add_multiple_pending_tasks(self, filtered[0])
        TaskScheduler.add_multiple_active_tasks(self, filtered[1])

        self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_tasks()) # to fix this implementation

    def filter_passed_tasks(self, todos):
        pending_tasks = []
        active_tasks = []

        for todo in todos:
            if self.passed_todo(todo):
                active_tasks.append(todo)
            else:
                pending_tasks.append(todo)
        return (pending_tasks, active_tasks)

    def activate_pending_task(self, task):
        TaskScheduler._activate_task(self, task)
        self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_tasks())

    def sorted_tasks(self):
        return sorted(self.active_tasks, key=lambda t: t.priority)

    def export_ical(self):
        self.file_worker.update_ical_file(self.active_tasks)

    def handle_tasks(self, tasks):
        for task in tasks:
            self.activate_pending_task(task)

    def has_moment(self, moment):
        for key in self.todos.keys():
            if key < moment or key is moment:
                return True
        return False

    def handle_moment(self, moment):
        for key in self.todos.keys():
            if key < moment:
                self.handle_tasks(self.todos[key])

# todo to make a new class to work with the files, file_worker
# todo: to create a new class inheriting arrow in order to make its objects hashable