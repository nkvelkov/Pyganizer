import unittest
from event_scheduler import EventScheduler
from event import Event
import arrow


class EventSchedulerTestCase(unittest.TestCase):
    def setUp(self):
        self.event_scheduler = EventScheduler()
        self.tz = 'local'
        self.start_datetime = arrow.Arrow(2015, 12, 12, 11,
                                          11, 11, tzinfo=self.tz)
        self.end_datetime = arrow.Arrow(2015, 12, 13, 11, 11, 11, tzinfo=self.tz)
        self.test_datetime = self.end_datetime.replace(hours=+1)
        self.event = Event(self.start_datetime, self.end_datetime, "name",
                           "message", 'pending', 1, self.tz)

class TestEventScheduler(EventSchedulerTestCase):

    def test_add_event(self):
        event = self.event_scheduler.add_event(self.start_datetime, self.end_datetime,
                                       "name", "message", self.tz)

        first_datetime = event in self.event_scheduler.todos[self.event.start_datetime]
        second_datetime = event in self.event_scheduler.todos[self.event.deadline_datetime]

        self.assertTrue(first_datetime and second_datetime)

    def test_add_multiple_active_events(self):
        second_event = self.event
        second_event.deadline_datetime = self.test_datetime

        self.event_scheduler.add_multiple_active_events([second_event, self.event])

        first_in = self.event in self.event_scheduler.active_todos 
        second_in = second_event in self.event_scheduler.active_todos

        self.assertTrue(first_in and second_in)

    def test_add_multiple_pending_events(self):
        second_event = self.event
        second_event.deadline_datetime = self.test_datetime
        
        self.event_scheduler.add_multiple_pending_events([second_event, self.event])

        keys = self.event_scheduler.todos.keys()
        start_in = self.event.start_datetime in keys
        deadline_in = self.event.deadline_datetime in keys
        second_start_in = second_event.start_datetime in keys
        second_deadline_in = second_event.deadline_datetime in keys

        self.assertTrue(start_in and deadline_in and second_start_in and second_deadline_in)

    def test_queue_event(self):
        self.event_scheduler.queue_event(self.event)

        start_in = self.event.start_datetime in self.event_scheduler.todos.keys()
        deadline_in = self.event.deadline_datetime in self.event_scheduler.todos.keys()

        self.assertTrue(start_in and deadline_in)

    def test_activate_event(self):
        self.event_scheduler.activate_event(self.event)

        is_active = self.event.mode is 'active'
        transferred = self.event in self.event_scheduler.active_todos
        removed = self.event.start_datetime not in self.event_scheduler.todos.keys()

        self.assertTrue(is_active and transferred and removed)

    def test_add_event_by_date(self):
        self.event_scheduler.add_event_by_date(self.event.start_datetime, self.event)

        self.assertTrue(self.event in self.event_scheduler.todos[self.event.start_datetime])

    def test_expire_active_event(self):
        self.event_scheduler.queue_event(self.event)
        self.event_scheduler.activate_event(self.event)
        self.event_scheduler.expire_active_event(self.event)

        removed = self.event.deadline_datetime not in self.event_scheduler.todos.keys()
        in_active_events = self.event in self.event_scheduler.active_events
       
        self.assertTrue(removed and not in_active_events)

    def test_remove_empty_entries(self):
        todos = self.event_scheduler.todos
        todos['1'] = []
        todos['2'] = []

        self.event_scheduler.remove_empty_entries()

        one = self.event_scheduler.todos.get('1') is None
        two = self.event_scheduler.todos.get('2') is None

        self.assertTrue(one and two)


if __name__ == '__main__':
    unittest.main()
