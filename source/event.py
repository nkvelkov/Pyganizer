from arrow_encoder import ArrowEncoder, as_arrow
import icalendar
from icalendar import Calendar
import json
import arrow

class Event:
    def __init__(self, start_datetime, deadline_datetime, name, message, mode, eid):
        self.start_datetime = start_datetime
        self.deadline_datetime = deadline_datetime
        self.name = name
        self.message = message
        self.mode = mode
        self.eid = eid

    def encode(self):
        return json.dumps(self, cls=EventEncoder)

    @staticmethod
    def decode(string):
        return json.loads(string, object_hook=as_event)

    def __str__(self):
        return "id: {}, starts: {}, ends: {}, name: {}, message: {}".format(
                self.eid, self.start_datetime.humanize(),
                self.deadline_datetime.humanize(),
                self.name, self.message
                )

    def to_ical(self):
        ical_event = icalendar.Event()
        ical_event.add('dtstart', self.start_datetime.naive)
        ical_event.add('dtend', self.deadline_datetime.naive)
        ical_event.add('summary', self.encode())
        ical_event['uid'] = self.name

        return ical_event

class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            start_datetime = json.dumps(obj.start_datetime, cls=ArrowEncoder)
            deadline_datetime = json.dumps(obj.deadline_datetime, cls=ArrowEncoder)

            return {"__event__": True,
                   "start_datetime": start_datetime,
                   "deadline_datetime": deadline_datetime,
                   "name": obj.name, "message": obj.message,
                   "mode": obj.mode, "eid": obj.eid}

        return json.JSONEncoder.default(self, obj)


def as_event(dct):
    if '__event__' in dct:
        dct.pop('__event__')
        decoded_datetime = json.loads(dct['start_datetime'], object_hook=as_arrow)
        dct['start_datetime'] = decoded_datetime

        decoded_datetime = json.loads(dct['deadline_datetime'], object_hook=as_arrow)
        dct['deadline_datetime'] = decoded_datetime
        return Event(**dct)
    return dct

