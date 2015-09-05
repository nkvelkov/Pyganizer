import datetime
import event
import threading
from event import Event
from task import Task
import time
import calendar   # to add Leap Year notification!
import arrow
from dateutil import tz


class TaskScheduler:
    def __init__(self):
        self.todos = {}
        self.active_tasks = []

    def append_task(self, start_date, name, message,
                    completeness, priority=1,
                    timezone='local'):
        current_moment = arrow.now()

        if start_date.to('utc') < current_moment.to('utc'):
            start_date = current_moment
            timezone = 'local'

        if not start_date in self.todos.keys():
            self.todos[start_date] = []

        target_id = self.get_id()
        target_task = Task(start_date, name, message,
                           completeness, priority,
                           target_id, timezone)
        self.todos[start_date].append(target_task)

        return target_task

    def add_multiple_active_tasks(self, tasks):
        self.active_tasks.extend(list(tasks))

    def add_multiple_pending_tasks(self, tasks):
        for task in tasks:
            self.insert_task(task)

    def insert_task(self, task):
        if not task.datetime in self.todos.keys():
            self.todos[task.datetime] = []
        task.tid = self.get_id()
        self.todos[task.datetime].append(task)

    def _activate_task(self, task):
        self.remove_pending_task(task)
        self.active_tasks.append(task)

    def find_pending_task(self, tid):
        for key in self.todos.keys():
            for todo in self.todos[key]:
                if todo.tid == tid:
                    return todo
        return None

    def find_active_task(self, target_id):
        for todo in self.active_tasks:
            if todo.tid == target_id:
                return todo
        return None

    def update_task(self, todo, progress):
        todo.completeness -= progress
        if todo.completeness <= 0:
            self.remove_todo(todo)
            return None
        else:
            return todo

    def add_task_progress_by_id(self, target_id, progress):
        task = self.find_active_task(target_id)
        if task is not None:
            self.active_tasks.remove(task)
            result_task = self.update_task(task, progress)
            if result_task is not None:
                self.active_tasks.append(task)
            return True
        return False

    def add_task_priority_by_id(self, target_id, priority):
        task = self.find_active_task(target_id)
        if task is not None:
            task.priority = priority
            return True
        return False

    def remove_pending_task(self, task):
        key = task.datetime
        if key in self.todos.keys():
            self.todos[key].pop(self.todos[key].index(task))
            self.remove_empty_entries()

    def remove_by_id(self, target_id):
        task = self.find_active_task(target_id)
        if task is not None:
            self.remove_todo(task)
            return True
        return False

    def remove_todo(self, todo):
        key = todo.datetime
        if key in self.todos.keys():
            if todo in self.todos[key]:
                self.todos[key].pop(self.todos[key].index(todo))
                self.remove_empty_entries()

        if todo in self.active_tasks:
            self.remove_active_task(todo)

    def add_task_progress_by_name(self, date, name, progress):
        for todo in self.todos[date]:
            if todo.name == name:
                self.add_task_progress(todo, progress)

    def get_id(self):
        result_id = 1
        with open("work_files/task_id.txt", "r") as f:
            saved_id = f.readline()
            if saved_id.isnumeric():
                result_id = int(saved_id) + 1

        with open("work_files/task_id.txt", "w") as f:
            f.write(str(result_id))

        return result_id

    def remove_active_task(self, task):
        self.active_tasks.pop(self.active_tasks.index(task))

    def remove_empty_entries(self):
        keys = self.todos.keys()
        self.todos = {
            key: self.todos[key] for key in keys if self.todos[key] != []
        }

    def enumerate_todos(self):
        result = []
        for holder in self.todos.values():
            for todo in holder:
                result.append(todo)
        return result

    def passed_date(self, target_date):
        current_moment = arrow.now()
        return target_date.to('utc') < current_moment.to('utc')

    def enumerate_todos(self):
        result = []
        for holder in self.todos.values():
            for todo in holder:
                result.append(todo)
        return result

    def passed_date(self, target_date):
        current_moment = arrow.now()
        return target_date.to('utc') < current_moment.to('utc')

    def passed_todo(self, task):
        return self.passed_date(task.datetime)
