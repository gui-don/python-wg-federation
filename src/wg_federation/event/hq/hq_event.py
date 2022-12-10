from enum import Enum


class HQEvent(str, Enum):
    """
    HQ events
    """

    BOOTSTRAPPED = 'bootstrapped'

    ANY_INTERFACE_CHANGED = 'any_interface_changed'

    INTERFACE_RELOADED = 'interface_reloaded'
    INTERFACE_CREATED = 'interface_created'
    INTERFACE_UPDATED = 'interface_updated'
    INTERFACE_DELETED = 'interface_deleted'

    FORUM_INTERFACE_RELOADED = 'forum_reloaded'
    FORUM_INTERFACE_CREATED = 'forum_created'
    FORUM_INTERFACE_UPDATED = 'forum_updated'
    FORUM_INTERFACE_DELETED = 'forum_deleted'

    PHONE_LINE_INTERFACE_RELOADED = 'phone_line_reloaded'
    PHONE_LINE_INTERFACE_CREATED = 'phone_line_created'
    PHONE_LINE_INTERFACE_UPDATED = 'phone_line_updated'
    PHONE_LINE_INTERFACE_DELETED = 'phone_line_deleted'
