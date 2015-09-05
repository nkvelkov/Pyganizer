import unittest
from task_scheduler import TaskScheduler
from task import Task
import arrow


class TaskSchedulerTestCase(unittest.TestCase):
    def setUp(self):
        self.task_scheduler = TaskScheduler()
        self.tz = 'local'
        self.datetime = arrow.Arrow(2015, 5, 9, 11, 11, 11, tzinfo=self.tz)
        self.task = Task(self.datetime, "name", "message", 100, 1, 1, self.tz)

class TestTaskScheduler(TaskSchedulerTestCase):
    
    def test_add_task(self):
        now = arrow.now()
        task = self.task_scheduler.append_task(now, "name", "message", 100, 1, self.tz)

        self.assertTrue(task in self.task_scheduler.todos[task.datetime])

    def test_add_multiple_active_tasks(self):
        test_task = self.task
        test_task.datetime = arrow.now()

        self.task_scheduler.add_multiple_active_tasks([test_task, self.task])

        self.assertTrue(test_task in self.task_scheduler.active_tasks and 
                        self.task in self.task_scheduler.active_tasks)

    def test_add_multiple_pending_tasks(self):
        test_task = self.task
        test_task.datetime = arrow.now()

        self.task_scheduler.add_multiple_pending_tasks([test_task, self.task])

        test_task_in = test_task in self.task_scheduler.todos[test_task.datetime]
        task_in = self.task in self.task_scheduler.todos[self.task.datetime]

        self.assertTrue(test_task_in and task_in)

    def test_activate_task(self):
        self.task_scheduler.insert_task(self.task)
        self.task_scheduler._activate_task(self.task)

        in_active_tasks = self.task in self.task_scheduler.active_tasks
        removed = self.task.datetime not in self.task_scheduler.todos.keys()

        self.assertTrue(in_active_tasks and removed)

    def test_add_task_progress_by_id(self):
        self.task_scheduler.insert_task(self.task)
        self.task_scheduler.add_task_progress_by_id(self.task.tid, 110)

        is_finished = self.task.datetime in self.task_scheduler.todos
        self.assertTrue(is_finished)

    def test_find_pending_task(self):
        self.task_scheduler.insert_task(self.task)
        self.assertTrue(self.task.datetime in self.task_scheduler.todos.keys())
    
    def test_add_task_progress_by_id_(self):
        self.task_scheduler.insert_task(self.task)
        self.task_scheduler._activate_task(self.task)
        self.task_scheduler.add_task_progress_by_id(self.task.tid, 10)

        result_task = self.task_scheduler.find_active_task(self.task.tid)

        self.assertEqual(result_task.completeness, 90)
    
if __name__ == '__main__':
    unittest.main()