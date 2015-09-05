import unittest
import arrow
import threading
import json
from arrow_encoder import ArrowEncoder, as_arrow
from task import Task, TaskEncoder, as_task


class TaskTestCase(unittest.TestCase):
    def setUp(self):
        self.tz = 'local'
        self.datetime = arrow.Arrow(2015, 5, 9, 11, 11, 11, tzinfo=self.tz)
        self.task = Task(self.datetime, "name", "message", 100, 1, 1, self.tz)


class TestEvent(TaskTestCase):

    def test_encode(self):
        encoded_task = self.task.encode()
        expected_json = json.dumps(self.task, cls=TaskEncoder)

        self.assertEqual(encoded_task, expected_json)
        
    def test_decode(self):
        test_json = self.task.encode()
        decoded_task = Task.decode(test_json)

        self.assertTrue(decoded_task == self.task)


if __name__ == '__main__':
    unittest.main()