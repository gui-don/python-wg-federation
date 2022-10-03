from enum import Enum


class Status(int, Enum):
    """
    Controller result
    """
    SUCCESS = 0
    DEFAULT_ERROR = 1
