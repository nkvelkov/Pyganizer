from task_organizer import TaskOrganizer
from file_worker import FileWorker


class Pyganizer(TaskOrganizer):
    def __init__(self, pending_tasks, activate_tasks):
        super().__init__(pending_tasks, activate_tasks)
        self.termination_flag = False

    def execute(self):
        thread = threading.Thread(target=self.start_execution)
        thread.start()

    def start_execution(self):
        self.termination_flag = False

        while not self.termination_flag:
            current_moment = arrow.utcnow().to('local')
            # current_moment = self.get_date(utc)

            if self.todos.get(current_moment) is not None:
                self.activate_task(current_moment)

            time.sleep(1)

    def terminate(self):
        self.termination_flag = True  # lock or atomic


# self.add_saved_tasks()
# to create destructor
