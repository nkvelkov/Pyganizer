import datetime
import event
import threading
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow


class TaskScheduler:
    def __init__(self):
        self.todos = {}
        self.active_tasks = []
        self.id = 0;

    def passed_date(self, target_date):
        current_moment = arrow.utcnow().to('local')

        return target_date < current_moment

    def add_task(self, start_date, name, message, completeness, priority=1):
        if passed_date(start_date):
            start_date = arrow.utcnow.to('local')

        if not start_date in self.todos.keys():
            self.todos[start_date] = []

        target_id = self.get_id()
        target_task = Task(start_date, name, message, completeness, priority, target_id)
        self.todos[start_date].append(target_task)

        return target_task

    def add_task_progress(self, todo, progress):
        todo.completeness -= progress
        if todo.completeness <= 0:
            self.remove_todo(todo)

    def find_pending_task(self, tid):
        for key in self.todos.keys():
            for todo in self.todos[key]:
                if todo.tid = tid:
                    return todo
        return None

    def find_active_task(self, target_id):
        for todo in self.active_tasks:
            if todo.tid == target_id:
                return todo
        return None

    def add_task_progress_by_id(self, target_id, progress):
        task = self.find_active_task(target_id)
        if task not None:
            self.add_task_progress(task, progress)
            return True
        return False

    def add_task_priority_by_id(self, target_id, priority):
        task = self.find_active_task(target_id)
        if task is not None:
            task.priority = priority
            return True
        return False

    def remove_by_id(self, target_id):
        task = self.find_active_task(target_id)
        if task is not None:
            remove_todo(todo)
            return True
        return False
        
    def add_multiple_active_tasks(self, tasks):
        self.active_tasks.extend(list(tasks))

    def add_multiple_pending_tasks(self, tasks):
        for task in tasks:
            self.insert_task(task)

    def remove_pending_task(task):
        key = task.datetime

        if key in self.todos.keys():
            self.todos[key].pop(self.todos[key].index(todo))
            self.remove_empty_entries()

    def remove_todo(self, todo):
        key = todo.datetime

        if key in self.todos.keys():
            self.todos[key].pop(self.todos[key].index(todo))
            self.remove_empty_entries()

        if todo in self.active_tasks:
            self.remove_active_task(todo)

    def remove_by_name(self, key, name):
        for todo in self.todos[key]:
            if todo.name == name:
                remove_todo(todo)
                return True
        return False

    def add_task_progress_by_name(self, date, name, progress):
        for todo in self.todos[date]:
            if todo.name == name:
                self.add_task_progress(todo, progress)

    def insert_task(self, task):
        if not task.date in self.todos.keys():
            self.todos[task.date] = []
        task.id = self.get_id()
        self.todos[task.date].append(task)

    def remove_empty_entries(self):
        keys = self.todos.keys()
        {key: self.todos[key] for key in keys if self.todos[key] != []}

    def get_id(self):
        self.id = self.id + 1
        return self.id

    def remove_active_task(self, task):
        self.active_tasks.pop(self.active_tasks.index(task))

    def passed_todo(self, task):
        return self.passed_date(task.datetime)

    def activate_task(self, task):
        self.remove_pending_task(task)
        self.active_tasks.append(task)



# todo to make a new class to work with the files, file_worker
# todo: to create a new class inheriting arrow in order to make its objects hashable