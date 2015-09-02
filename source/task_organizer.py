import datetime
import event
import threading
from task_scheduler import TaskScheduler
from file_worker import FileWorker
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow


class TaskOrganizer(TaskScheduler):
    def __init__(self, pending_tasks, active_tasks):
        super().__init__()
        self.file_worker = FileWorker(pending_tasks, active_tasks)
        self.init_id()

    def add_task(self, start_date, name, message, completeness, priority=1):
        print(type(start_date))
        task = self.append_task(start_date, name, message, completeness, priority)
        self.file_worker.add_todo(task)

    def add_task_progress(self, target_id, progress):
        result = TaskScheduler.add_task_progress_by_id(target_id, progress) # to implement proper exception handling
        if result:
            self.file_worker.update_active_file(self.sorted_tasks())
        return result

    def set_task_priority(self, target_id, priority):
        result = TaskScheduler.add_task_priority_by_id(target_id, priority) # to implement proper exception handling
        if result:
            self.file_worker.update_active_file(self.sorted_tasks())
        return result

    def remove_task(self, target_id):
        result = TaskScheduler.remove_by_id(target_id)
        if result:
            self.file_worker.update_active_file(self.sorted_tasks())
        return result

    def load_saved_tasks(self):
        self.load_saved_active_tasks()
        self.load_saved_pending_tasks()

    def load_saved_active_tasks(self):
        tasks = self.file_worker.get_saved_active_todoes()
        TaskScheduler.add_multiple_active_tasks(tasks)

    def load_saved_pending_tasks(self):
        todos = self.file_worker.get_saved_pending_todos()
        filtered = self.filter_passed_todos(todos)

        TaskScheduler.add_multiple_pending_tasks(filtered[0])
        TaskScheduler.add_multiple_active_tasks(filtered[1])

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
        TaskScheduler.activate_task(task)
        self.file_worker.update_all_files(self.enumerate_todos(), self.sorted_tasks())

    def handle_tasks(self, tasks):
        for task in tasks:
            self.active_tasks(task)

    def sorted_tasks(self):
        return sorted(self.active_tasks, key=lambda t: t.priority)

    def init_id(self):
        with open("task_id.txt", "r") as f:
            saved_id = f.readline()
            self.id = int(saved_id)

    def export_ical(self):
        pass

    def __del__(self):
        with open("task_id.txt", "w") as f:
            f.write("{}".format(self.id+1))

# todo to make a new class to work with the files, file_worker
# todo: to create a new class inheriting arrow in order to make its objects hashable