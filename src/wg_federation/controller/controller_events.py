from enum import Enum


class ControllerEvents(Enum):
    """
    Controller events
    """

    CONTROLLER_BASELINE = 'controller_baseline'
    CONTROLLER_MAIN = 'controller_main'
    CONTROLLER_LATE = 'controller_late'
