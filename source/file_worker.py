from task import Task
from event import Event
from task_encoder import TaskEncoder, as_task
from event_encoder import EventEncoder, as_event
import json


class FileWorker:
    def __init__(pending_todos, active_todos, encoder):
        self.encoder = encoder
        self.pending_todos = pending_todos
        self.active_todos = active_todos

    def add_todo(self, todo):
        with open(self.pending_todos, "r+") as f:
            encoded = json.dumps(todo, cls=self.encoder)
            f.append("{}\n".format(encoded))

    def encode_todos(self, todos):
        result = []
        for todo in todos:
            encoded = json.dumps(todo, cls=self.encoder)
            result.append(encoded)
        return result

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
                task = json.loads(line, object_hook=as_task)
            else:
                event = json.loads(line, object_hook=as_event)
            result.append(task)
        return result

    def update_active_file(self, todos):
        write_content = self.encode_todos()
        with open(self.active_todoes, "w") as f:
            for encoded in write_content:
                f.write("{}\n".format(encoded))

    def update_pending_file(self, todos):
        with open(self.pending_todos, "w") as f:            
            for todo in pending_todos:
                self.add_todo(todo)
    
    def update_all_files(pending_todos, active_todos):
        self.update_files(active_todos)
        self.update_pending_file(pending_todos)
