from enum import Enum


class LogLevel(str, Enum):
    """
    Enum of possible LogLevels
    """
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'
