import unittest
from pyganizer import Pyganizer
import arrow
import threading
import time
from task import Task


class TestPyganizer(unittest.TestCase):

    def test_execute(self):
        organier = Pyganizer()
        utc = arrow.utcnow().to('local')

        signal_time = 2
        message = 'test_message'
        event = 'test_event'

        utc_date = utc.replace(seconds=+signal_time)
        utc_date = organier.get_date(utc_date)

        organier.execute()
        organier.add_event(utc_date, event, message, alert_seconds=1)

        time.sleep(signal_time+2)

        organier.terminate()

        answer = False
        with open('passed_data.txt', 'r+') as f:
            target_message = "{} {}\n".format(event, message)
            added_moments = f.readlines()
            if target_message in added_moments:
                answer = True

        self.assertTrue(answer)

    def test_addition_to_active_tasks(self):
        organier = Pyganizer()
        organier.execute()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+2)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name'
        task_message = 'task_message'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, 2*progress, priority)
        organier.insert_task(task)

        time.sleep(3)
        organier.terminate()

        self.assertTrue(task in organier.active_tasks)

    def test_calculate_date(self):
        organier = Pyganizer()
        utc = arrow.utcnow().to('local')

        alert_hours = 1
        date = organier.get_date(utc)

        respond = organier.calculate_date(date, alert_hours=alert_hours)

        expected_date = utc.replace(seconds=+1)

        self.assertEqual(organier.get_date(expected_date), respond)

    def test_stringify(self):
        organier = Pyganizer()

        utc = arrow.utcnow().to('local')
        utc = utc.replace(seconds=+1)

        utc_date = organier.get_date(utc)

        message = 'task_message'
        task = 'task_event'
        comleteness = 50
        priority = 1

        organier.add_task(utc_date, task, message, comleteness, priority)

        result_string = "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}".format(
            'task', utc_date[0], utc_date[1], utc_date[2], utc_date[3],
            utc_date[4], utc_date[5], task, message, comleteness, priority
        )
        self.assertEqual(result_string, organier.stringify(utc_date))

    def test_add_event(self):
        organier = Pyganizer()

        utc = arrow.utcnow().to('local')
        target_date = organier.get_date(utc.replace(hours=+3))

        message = 'test_message'
        event = 'test_event'

        organier.add_event(target_date, event, message, alert_hours=2)

        result_event = (organier.todos.get(target_date) is not None)
        alert_moment = organier.calculate_date(target_date, alert_hours=2)
        alert_event = (organier.todos.get(alert_moment) is not None)

        self.assertTrue(result_event and alert_event)

    def test_add_task(self):
        organier = Pyganizer()

        utc = arrow.utcnow().to('local')
        target_date = organier.get_date(utc.replace(hours=+3))

        message = 'task_message'
        name = 'task_name'

        organier.add_task(target_date, name, message, 50, 1)

        result_task = organier.todos.get(target_date) is not None

        self.assertTrue(result_task)

    def test_stringify_date(self):
        organier = Pyganizer()

        utc = arrow.utcnow().to('local')
        date = organier.get_date(utc)

        expected_result = "{0} {1} {2} {3} {4} {5}".format(
            date[0], date[1], date[2], date[3], date[4], date[5]
        )

        self.assertEqual(expected_result, organier.stringify_date(date))

    def test_get_date(self):
        organier = Pyganizer()

        utc = arrow.utcnow().to('local')
        date = organier.get_date(utc)

        expected_date = (utc.day, utc.month, utc.year,
                         utc.hour, utc.minute, utc.second)

        self.assertEqual(expected_date, date)

    def test_add_task_progress(self):
        organier = Pyganizer()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+2)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name'
        task_message = 'task_message'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, 2*progress, priority)

        organier.insert_task(task)
        organier.add_task_progress(task, progress)

        respond = organier.get_todo(start_date, task_name)
        self.assertEqual(respond.completeness, 50)

    def test_add_task_completion(self):
        organier = Pyganizer()
        organier.execute()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+2)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name'
        task_message = 'task_message'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, progress, priority)
        organier.insert_task(task)

        time.sleep(3)
        organier.terminate()

        organier.add_task_progress(task, progress)

        removed_from_todos = organier.get_todo(start_date, task_name) is None
        removed_from_active_todos = task not in organier.active_tasks

        self.assertTrue(removed_from_todos)
        self.assertTrue(removed_from_active_todos)

    def test_add_task_completion_by_name(self):
        organier = Pyganizer()
        organier.execute()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+2)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name'
        task_message = 'task_message'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, progress, priority)
        organier.insert_task(task)

        time.sleep(3)
        organier.terminate()

        organier.add_task_progress_by_name(start_date, task_name, progress)

        removed_from_todos = organier.get_todo(start_date, task_name) is None
        removed_from_active_todos = task not in organier.active_tasks

        self.assertTrue(removed_from_todos)
        self.assertTrue(removed_from_active_todos)

    def test_remove_todo(self):
        organier = Pyganizer()
        organier.execute()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+1)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name'
        task_message = 'task_message'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, progress, priority)

        organier.insert_task(task)
        time.sleep(1)
        organier.terminate()

        organier.remove_todo(task)

        response = organier.todos.get(start_date)

        self.assertTrue(response is None or task not in response)

    def test_remove_by_name(self):
        organier = Pyganizer()
        organier.execute()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+1)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name'
        task_message = 'task_message'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, progress, priority)

        organier.insert_task(task)
        time.sleep(1)
        organier.terminate()

        organier.remove_by_name(start_date, task_name)

        response = organier.todos.get(start_date)

        self.assertTrue(response is None or task not in response)

    def test_name_exist(self):
        organier = Pyganizer()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+1)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name'
        task_message = 'task_message'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, progress, priority)
        organier.insert_task(task)

        self.assertTrue(organier.name_exists(start_date, task_name))

    def test_name_not_exist(self):
        organier = Pyganizer()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+1)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name'
        task_message = 'task_message'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, progress, priority)
        organier.insert_task(task)

        self.assertFalse(organier.name_exists(start_date, task_message))

    def test_add_to_active_tasks_file(self):
        organier = Pyganizer()
        organier.execute()

        utc = arrow.utcnow().to('local')
        utc_date = utc.replace(seconds=+1)
        start_date = organier.get_date(utc_date)

        task_name = 'task_name_active'
        task_message = 'task_message_active'
        progress = 50
        priority = 1

        task = Task(start_date, task_name, task_message, progress, priority)
        organier.insert_task(task)

        time.sleep(3)

        with open("active_tasks.txt", "r") as f:
            active_tasks = f.readlines()
            self.assertTrue("{}\n".format(str(task)) in active_tasks)

        organier.terminate()


if __name__ == '__main__':
    unittest.main()
