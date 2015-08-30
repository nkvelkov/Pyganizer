import datetime
import event
import threading
from task_scheduler import TaskScheduler
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow
from taks_encoder import TaskEncoder


class TaskOrganizer(TaskScheduler):
    def __init__(self, pending_tasks, active_tasks):
        super().__init__()
        self.file_worker = FileWorker(pending_tasks, active_tasks, TaskEncoder)
        self.init_id()

    def add_task(self, start_date, name, message, completeness, priority=1):
        task = TaskScheduler.add_task(start_date, name, message, completeness, priority):
        self.file_worker.add_todo(task)

    def add_task_progress(self, target_id, progress):
        result = TaskScheduler.add_task_progress_by_id(target_id, progress) # to implement proper exception handling
        self.file_worker.update_active_file(self.active_tasks)
        return result

    def set_task_priority(self, target_id, priority):
        result = TaskScheduler.add_task_priority_by_id(target_id, priority) # to implement proper exception handling
        self.file_worker.update_active_file(self.active_tasks)
        return result

    def remove_task(self, target_id):
        result = TaskScheduler.remove_by_id(target_id)
        self.file_worker.update_active_file(self.active_tasks)
        return result

    def load_saved_active_tasks(self):
        tasks = self.file_worker.get_saved_active_todoes()
        TaskScheduler.add_multiple_active_tasks(tasks)

    def load_saved_pending_tasks(self):
        todos = self.file_worker.get_saved_pending_todos()

        filtered = self.filter_passed_todos(todos)
        TaskScheduler.add_multiple_pending_tasks(filtered[0])
        TaskScheduler.add_multiple_active_tasks(filtered[1])

        self.file_worker.update_all_files(self.todos, self.active_events) # to fix this implementation

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
        self.file_worker.update_all_files(self.todos, self.active_events)

    def init_id(self):
        with open("task_id.txt", "r") as f:
            saved_id = f.readline()
            self.id = int(saved_id)

    def __del__(self):
        with open("task_id.txt", "w") as f:
            f.write("{}".format(self.id+1))

# todo to make a new class to work with the files, file_worker
# todo: to create a new class inheriting arrow in order to make its objects hashable