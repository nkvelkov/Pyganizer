import threading
from task_organizer import TaskOrganizer
from event_organizer import EventOrganizer
from file_worker import FileWorker


class Pyganizer():
    def __init__(self, pending_tasks, active_tasks, pending_events, active_events):
        self.termination_flag = False
        self.task_organizer = TaskOrganizer(pending_tasks, active_tasks)
        self.task_lock = threading.Lock()

        self.event_organizer = EventOrganizer(pending_events, active_events)
        self.event_lock = threading.Lock()

    def prepare_tasks(self):
        self.task_lock.acquire()
        self.task_organizer.load_saved_tasks()
        self.task_lock.release()

    def prepare_events(self):
        self.event_lock.acquire()
        self.event_organizer.load_saved_events(event_value) 
        self.event_lock.release()

    def execute(self):
        self.prepare_tasks()
        self.prepare_events()

        thread = threading.Thread(target=self.start_execution)
        thread.start()

    def start_execution(self):
        self.termination_flag = False

        while not self.termination_flag:
            current_moment = arrow.utcnow().to('local')
            task_value = self.task_organizer.todos.get(current_moment)
            event_value = self.event_organizer.todos.get(current_moment)

            if task_value is not None and task_value is not []:
                self.task_lock.acquire()
                self.task_organizer.handle_tasks(task_value)
                self.task_lock.release()

            if event_value is not None and event_value is not []:
                self.event_lock.acquire()
                self.event_organizer.handle_events(event_value) 
                self.event_lock.release()

            time.sleep(1)

    def terminate(self):
        self.termination_flag = True  # lock or atomic

    def add_task(self, start_date, name, message, comleteness, priority):
        self.task_lock.acquire()
        print(type(start_date))
        self.task_organizer.add_task(start_date, name, message, comleteness, priority)
        self.task_lock.release()
    
    # to check that out
    def __del__(self):
        self.terminate()

# self.add_saved_tasks()
# to create destructor
