from task import Task
from event import Event
import json


class FileWorker:
    def __init__(self, pending_todos, active_todos, passed_todos=None):
        self.pending_todos = pending_todos
        self.active_todos = active_todos
        self.passed_todos = passed_todos

    def add_todo(self, todo):
        with open(self.pending_todos, "a") as f:
            f.write("{}\n".format(todo.encode()))

    def get_saved_active_todos(self):
        with open(self.active_todoes, "r") as f:
            lines = f.readlines()
            todos = self.decode_todos(lines)
            return todos

    def get_saved_pending_todos(self):
        with open(self.pending_todoes, "r") as f:
            lines = f.readlines()
            todos = self.decode_todos(lines)
            return todos

    def decode_todos(self, lines):
        result = []
        for line in lines:
            if line.find("__task__"):
                todo = Task.decode(line)
            else:
                todo = Event.decode(line)
            result.append(todo)
        return result

    def encode_todos(self, todos):
        result = []
        for todo in todos:
            result.append(todo.encode())
        return result

    def update_active_file(self, todos):
        write_content = self.encode_todos(todos)
        with open(self.active_todoes, "w") as f:
            for encoded in write_content:
                f.write("{}\n".format(encoded))

    def update_pending_file(self, pending_todos):
        with open(self.pending_todos, "w") as f:            
            for todo in pending_todos:
                f.write("{}\n".format(todo.encode()))
    
    def update_all_files(pending_todos, active_todos):
        self.update_active_file(active_todos)
        self.update_pending_file(pending_todos)

    def update_passed_todos(self, passed_todos):
        with open(self.passed_todos, "a") as f:
            for todo in passed_todos:
                f.write("{}\n".format(todo.encode()))
