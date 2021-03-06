import icalendar
from icalendar import Calendar
from task import Task
from event import Event
import json


class FileWorker:
    def __init__(self, pending_todos, active_todos,
                 ical_file, passed_todos=None):
        self.pending_todos = pending_todos
        self.active_todos = active_todos
        self.ical_file = ical_file
        self.passed_todos = passed_todos

    def add_todo(self, todo):
        with open(self.pending_todos, "a") as f:
            f.write("{}\n".format(todo.encode()))

    def get_saved_active_todos(self):
        with open(self.active_todos, "r") as f:
            lines = f.readlines()
            todos = self.decode_todos(lines)
            return todos

    def get_saved_pending_todos(self):
        with open(self.pending_todos, "r") as f:
            lines = f.readlines()
            todos = self.decode_todos(lines)
            return todos

    def decode_todos(self, lines):
        result = []
        for line in lines:
            if line.find("__task__") != -1:
                todo = Task.decode(line)
            elif line.find("__event__") != -1:
                todo = Event.decode(line)
            result.append(todo)
        return result

    def encode_todos(self, todos):
        result = set()
        for todo in todos:
            result.add(todo.encode())
        return result

    def update_active_file(self, todos):
        write_content = self.encode_todos(todos)
        with open(self.active_todos, "w") as f:
            for encoded in write_content:
                f.write("{}\n".format(encoded))

    def update_pending_file(self, pending_todos):
        with open(self.pending_todos, "w") as f:
            for todo in pending_todos:
                f.write("{}\n".format(todo.encode()))

    def update_all_files(self, pending_todos, active_todos):
        self.update_active_file(active_todos)
        self.update_pending_file(pending_todos)

    def update_passed_todos(self, passed_todos):
        with open(self.passed_todos, "a") as f:
            for todo in passed_todos:
                f.write("{}\n".format(todo.encode()))

    def update_ical_file(self, active_todos):
        cal = Calendar()
        cal['summary'] = 'This calendar was generated by the Pyganizer!'

        for todo in active_todos:
            cal.add_component(todo.to_ical())

        with open(self.ical_file, "wb") as f:
            f.write(cal.to_ical())
