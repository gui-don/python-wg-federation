from enum import Enum


class Status(int, Enum):
    """
    Controller result
    """
    SUCCESS = 0
    NOT_RUN = -1
    DEFAULT_ERROR = 1
