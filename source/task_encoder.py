from task import Task
from arrow_encoder import ArrowEncoder, as_arrow
import json


class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            datetime = json.dumps(obj.datetime, cls=ArrowEncoder)
            return {"__task__": True, "tid": obj.tid, "datetime": datetime, "name": obj.name, "message": obj.message, "completeness": obj.completeness, "priority": obj.priority}
            # return [obj.date, obj.name, obj.message,
            #       obj.completeness, obj.priority]
        return json.JSONEncoder.default(self, obj)


def as_task(dct):
    if '__task__' in dct:
        dct.pop('__task__')
        decoded_datetime = json.loads(dct['datetime'], object_hook=as_arrow)
        dct['datetime'] = decoded_datetime
        return Task(**dct)
    return dct