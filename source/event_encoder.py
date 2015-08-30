from event import Event
from arrow_encoder import ArrowEncoder, as_arrow
import json


class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            datetime = json.dumps(obj.datetime, cls=ArrowEncoder)
            return {"__event__": True, "eid": obj.eid, "datetime": datetime, "name": obj.name, "message": obj.message, "mode": obj.mode}
            # return [obj.date, obj.name, obj.message,
            #       obj.completeness, obj.priority]
        return json.JSONEncoder.default(self, obj)


def as_event(dct):
    if '__event__' in dct:
        dct.pop('__event__')
        decoded_datetime = json.loads(dct['datetime'], object_hook=as_arrow)
        dct['datetime'] = decoded_datetime
        return Event(**dct)
    return dct