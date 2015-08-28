from scheduler import Scheduler
from file_worker import FileWorker


class Organizer(Scheduler):
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
