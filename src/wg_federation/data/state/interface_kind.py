from enum import Enum


class InterfaceKind(str, Enum):
    """
    Enum of possible WireGuard interfaces kind
    """
    INTERFACE = 'INTERFACE'  # Federation interface
    PHONE_LINE = 'PHONE_LINE'  # For HQ/Member meta communications
    FORUM = 'FORUM'  # For HQ/Candidate meta communications
