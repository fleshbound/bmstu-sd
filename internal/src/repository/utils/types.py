import bson
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


def object_id_from_int(n: int):
    s = str(n)
    s = '0' * (24 - len(s)) + s
    return bson.ObjectId(s)


def int_from_object_id(obj: ObjectId):
    return int(str(obj))


def int_from_pyobject_id(obj: ObjectId):
    return int(str(obj))
