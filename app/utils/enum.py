from enum import Enum


class EnumBase(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def name_list(cls):
        return list(map(lambda c: c.name, cls))
