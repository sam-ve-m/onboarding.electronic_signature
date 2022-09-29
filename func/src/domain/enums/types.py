# Standards
from enum import IntEnum


class QueueTypes(IntEnum):
    USER_SET_ELECTRONIC_SIGNATURE = 9

    def __repr__(self):
        return self.value
