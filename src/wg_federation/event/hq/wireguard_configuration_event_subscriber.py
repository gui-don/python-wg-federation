from enum import Enum

from wg_federation.data.state.wireguard_interface import WireguardInterface
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.observer.is_data_class import IsDataClass
from wg_federation.observer.status import Status


class WireguardConfigurationEventSubscriber(EventSubscriber):
    """ Creates/Updates WireGuard interfaces """

    def get_subscribed_events(self) -> list[Enum]:
        return [HQEvent.ANY_INTERFACE_CHANGED]

    def _do_run(self, data: IsDataClass) -> Status:
        return Status.SUCCESS

    @classmethod
    def support_data_class(cls) -> type:
        return WireguardInterface
