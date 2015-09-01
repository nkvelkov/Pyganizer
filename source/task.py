import json
from arrow_encoder import ArrowEncoder, as_arrow
import json


class Task:
    def __init__(self, datetime, name, message, completeness, priority, tid):
        self.datetime = datetime
        self.name = name
        self.message = message
        self.completeness = completeness
        self.priority = priority
        self.tid = tid

    def encode(self):
        return json.dumps(self, cls=TaskEncoder)

    @staticmethod
    def decode(string):
        return json.loads(string, object_hook=as_task)

    def add_progress(self, completeness):
        self.completeness -= completeness
 
    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.datetime, self.name, self.message, self.completeness, self.priority)
    
    def foo(self):
        return "{0} {1} {2} {3} {4}".format(
            self.date_to_string(), self.name, self.message,
            str(self.completeness), str(self.priority)
        )


class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            datetime = json.dumps(obj.datetime, cls=ArrowEncoder)
            return {"__task__": True, "tid": obj.tid, "datetime": datetime, "name": obj.name, "message": obj.message, "completeness": obj.completeness, "priority": obj.priority}
        return json.JSONEncoder.default(self, obj)


def as_task(dct):
    if '__task__' in dct:
        dct.pop('__task__')
        decoded_datetime = json.loads(dct['datetime'], object_hook=as_arrow)
        dct['datetime'] = decoded_datetime
        return Task(**dct)
    return dct