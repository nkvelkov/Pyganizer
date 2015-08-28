import datetime
import event
import threading
from task_scheduler import TaskScheduler
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow


class TaskOrganizer(TaskScheduler):
    def __init__(self, pending_events, pending_tasks, active_events, active_tasks):
        self.file_worker = FileWorker(pending_events, pending_tasks, active_events, active_tasks, 'id.txt')

    def add_event(self, deadline_date, start_date, name, message):
        if not Scheduler.add_event(deadline_date, start_date, name, message):
            return False # or raise apropriate exception

        self.file_worker.add_event(deadline_date, start_date, name, message)
        return True

    def add_task(self, start_date, name, message, completeness, priority=1):
        if not Scheduler.add_task(start_date, name, message, completeness, priority):
            return False

        self.file_worker.add_task(start_date, name, message, completeness, priority)
        return True

    def add_task_progress(self, target_id, progress):
        Scheduler.add_task_progress_by_id(target_id, progress) # to implement proper exception handling
        self.file_worker.update_task_files(self.active_tasks)

    def remove_task(self, target_id):
        Scheduler.remove_by_id(target_id)
        self.file_worker.update_task_files(self.todos, self.active_tasks)

    def remove_event(self, target_id):
        Scheduler.remove_by_id(target_id)
        self.file_worker.update_event_files(self.todos, self.active_events)

    def load_saved_tasks(self):
        tasks = self.file_worker.get_saved_tasks()
        Scheduler.add_multiple_taks(self.filter_passed_tasks(tasks))

    def load_saved_active_events(self):
        events = self.file_worker.get_saved_events()
        Scheduler.add_multiple_events(self.filter_passed_active_events(events))

    def load_saved_todos(self):
        todos = self.file_worker.get_saved_todos()
        Scheduler.add_multiple_todos(self.filter_passed_todos(todos))

    def filter_passed_todos(self, todos):
        pass
        self.file_worker.update_files(self.todos, self.active_events)

    def filter_passed_events(self):
        pass
        self.file_worker.update_files(self.todos, self.active_events)
        
    def add_task(self, start_date, name, message, completeness, priority=1):
        if passed_date(start_date)
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

        self.todos[key].pop(self.todos[key].index(todo))
        if todo in self.active_tasks:
            self.remove_active_task(todo)

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

    def remove_active_task(self, task):
        self.active_tasks.pop(self.active_tasks.index(task))

    def activate_task(self, task):
        if not self_has_todo(task):
            pass
        pass
        # self.activate_task.append(task)

# todo to make a new class to work with the files, file_worker
# todo: to create a new class inheriting arrow in order to make its objects hashable