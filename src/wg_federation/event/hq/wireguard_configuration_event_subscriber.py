from enum import Enum

from wg_federation.data.state.hq_state import HQState
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.observer.is_data_class import IsDataClass


class WireguardConfigurationEventSubscriber(EventSubscriber[HQState]):
    """ Creates/Updates WireGuard interfaces """

    def get_subscribed_events(self) -> list[Enum]:
        return [HQEvent.STATE_CREATED, HQEvent.STATE_UPDATED]

    def run(self, data: IsDataClass) -> IsDataClass:
        return data
