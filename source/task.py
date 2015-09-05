import json
from arrow_encoder import ArrowEncoder, as_arrow
import icalendar
from icalendar import Calendar

class Task:
    def __init__(self, datetime, name, message, completeness, priority, tid, timezone):
        self.datetime = datetime
        self.name = name
        self.message = message
        self.completeness = completeness
        self.priority = priority
        self.tid = tid
        self.timezone = timezone

    def encode(self):
        return json.dumps(self, cls=TaskEncoder)

    @staticmethod
    def decode(string):
        return json.loads(string, object_hook=as_task)
 
    def __str__(self):
        return "id: {}, starts: {}, name: {}, message: {}, completeness: {}, priority: {}".format(
                self.tid, self.datetime.humanize(),
                self.name, self.message,
                self.completeness, self.priority
                )

    def to_ical(self):
        ical_event = icalendar.Event()
        ical_event.add('dtstart', self.datetime.naive)
        ical_event.add('summary', self.encode())
        ical_event['uid'] = self.name

        return ical_event


class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            datetime = json.dumps(obj.datetime, cls=ArrowEncoder)

            return {"__task__": True, "tid": obj.tid,
                    "datetime": datetime, "name": obj.name,
                    "message": obj.message, "completeness": obj.completeness,
                    "priority": obj.priority, "timezone": obj.timezone}
        return json.JSONEncoder.default(self, obj)


def as_task(dct):
    if '__task__' in dct:
        dct.pop('__task__')
        decoded_datetime = json.loads(dct['datetime'], object_hook=as_arrow)
        print("original timezone")
        print(dct["timezone"])
        decoded_datetime.to(dct["timezone"])

        dct['datetime'] = decoded_datetime
        return Task(**dct)
    return dct