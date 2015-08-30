import arrow
import json


class ArrowEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, arrow.Arrow):
            return {"__arrow__": True, "year": obj.year,
                    "month": obj.month, "day": obj.day, "hour": obj.hour,
                    "minute": obj.minute, "second": obj.second}
        return json.JSONEncoder.default(self, obj)


def as_arrow(dct):
    if '__arrow__' in dct:
        dct.pop('__arrow__')
        return arrow.Arrow(**dct)
    return dct