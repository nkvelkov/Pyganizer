import threading
from task_organizer import TaskOrganizer
from event_organizer import EventOrganizer
from file_worker import FileWorker
from my_exceptions import InvalidDateError


class Pyganizer():
    def __init__(self, pending_tasks_file, active_tasks_file,
                 ical_tasks_file, pending_events_file,
                 active_events_file, ical_events_file):
        self.termination_flag = False
        self.task_organizer = TaskOrganizer(pending_tasks_file, active_tasks_file, ical_tasks_file)
        self.task_lock = threading.Lock()

        self.event_organizer = EventOrganizer(pending_events_file, active_events_file, ical_events_file)
        self.event_lock = threading.Lock()

        self.prepare_tasks()
        self.prepare_events()

    def execute(self):
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

    def prepare_tasks(self):
        self.task_lock.acquire()
        self.task_organizer.load_saved_tasks()
        self.task_lock.release()

    def add_task(self, start_date, name, message, comleteness, priority):
        self.task_lock.acquire()
        print(type(start_date))
        self.task_lock.release()

    def remove_task(self, tid):
        result = True
        self.task_lock.acquire()
        result = self.task_organizer.remove_task(tid) 
        self.task_lock.release()
        return result

    def set_task_priority(self, tid, priority):
        result = True
        self.task_lock.acquire()
        result = self.task_organizer.set_task_priority(tid, priority) 
        self.task_lock.release()
        return result

    def add_task_progress(self, tid, progress):
        result = True
        self.task_lock.acquire()
        result = self.task_organizer.add_task_progress(tid, progress) 
        self.task_lock.release()
        return result
    
    def export_tasks_ical(self):
        self.task_lock.acquire()
        self.task_organizer.export_ical()
        self.task_lock.release()

    def prepare_events(self):
        self.event_lock.acquire()
        self.event_organizer.load_saved_events() 
        self.event_lock.release()

    def add_event(self, start_datetime, end_datetime, name, message):
        self.event_lock.acquire()
        try:
            self.event_organizer.add_event(start_datetime, end_datetime, name, message) 
        except InvalidDateError:
            raise
        finally:
            self.event_lock.release()

    def remove_event(self, eid):
        result = True
        self.event_lock.acquire()
        result = self.event_organizer.remove_event(eid) 
        self.event_lock.release()
        return result

    def export_events_ical(self):
        self.event_lock.acquire()
        self.event_organizer.export_ical() 
        self.event_lock.release()

    # to check that out
    def __del__(self):
        self.terminate()

# self.add_saved_tasks()
# to create destructor
