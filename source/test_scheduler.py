import unittest
import arrow
from event import Event
from task import Task
from scheduler import Scheduler


class SchedulerTestCase(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()
        utc = arrow.utcnow().to('local')
        self.date = utc
        self.utc = utc.replace(seconds=+3)
        self.event_name = 'test_event'
        self.task_name = 'task_name'
        self.message = 'alert_message'
        self.event = Event(utc, 'test_event', 'alert_message', 'active')
        self.task = Task(utc, 'test_task', 'alert_message', 50, 1)
        self.organier = self.scheduler


class TestScheduler(SchedulerTestCase):
    def test_add_event(self):
        target_date = self.date.replace(hours=+3)
        self.organier.add_event(target_date, self.event,
                                self.message, alert_hours=2)

        result_event = (self.organier.todos.get(target_date) is not None)
        alert_moment = self.organier.calculate_date(target_date, alert_hours=2)
        alert_event = (self.organier.todos.get(alert_moment) is not None)
        print(self.organier.get_date(target_date))
        print(self.organier.get_date(alert_moment))
        print(result_event)
        print(alert_event)
        print(self.organier.todos.get(target_date))
        print(self.organier.todos.get(alert_moment))
        self.assertTrue(result_event and alert_event)
    
    def test_add_task(self):
        target_date = self.organier.get_date(self.date.replace(hours=+3))
        self.organier.add_task(target_date, self.task_name, self.message, 50, 1)
        result_task = self.organier.todos.get(target_date) is not None

        self.assertTrue(result_task)

    def test_insert_task(self):
        target_date = self.organier.get_date(self.date.replace(hours=+3))
        target_task = Task(target_date, self.task_name, self.message, 50, 1)
        self.organier.insert_task(target_task)

        result_task = self.organier.todos.get(target_date) is not None
        
        self.assertTrue(result_task)

    def test_calculate_current_date(self):
        cur = arrow.utcnow().to('local')
        respond = self.organier.calculate_date(
                    cur,
                    alert_hours=1
        )
        print("respond -> {}".format(respond))

        expected_date = self.date.replace(seconds=+1)

        print("expected_date -> {}".format(self.organier.get_date(expected_date)))
        
        self.assertEqual(self.organier.get_date(expected_date), respond)

    def test_calculate_date(self):
        utc = self.utc.replace(hours=+2)
        
        respond = self.organier.calculate_date(
                    utc,
                    alert_hours=1
        )
         
        expected_date = utc.replace(hours=-1)

        self.assertEqual(self.organier.get_date(expected_date), respond)

if __name__ == '__main__':
    unittest.main()
