import unittest
import arrow
import threading
import time
import json
from event import Event, EventEncoder, as_event


class EventTestCase(unittest.TestCase):
    def setUp(self):
        self.tz = 'local'
        self.start_datetime = arrow.Arrow(2015, 9, 5, 11,
                                          11, 11, tzinfo=self.tz)
        self.end_datetime = arrow.Arrow(2015, 9, 5, 11, 11, 11, tzinfo=self.tz)
        self.event = Event(self.start_datetime, self.end_datetime, "name",
                           "message", 'pending', 1, self.tz)


class TestEvent(EventTestCase):

    def test_encode(self):
        encoded = self.event.encode()
        expected = json.dumps(self.event, cls=EventEncoder)

        self.assertEqual(encoded, expected)

    def test_decode(self):
        test_json = self.event.encode()
        decoded = Event.decode(test_json)

        self.assertEqual(self.event, decoded)

if __name__ == '__main__':
    unittest.main()
