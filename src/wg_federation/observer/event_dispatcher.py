import logging
from enum import Enum

from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.observer.is_data_class import IsDataClass
from wg_federation.observer.status import Status
from wg_federation.utils.utils import Utils


class EventDispatcher:
    """
    Dispatches any kind of events through class implementing EventSubscriberInterfaces.
    EventSubscriberInterfaces classes must be previously registered.
    """
    _subscribers: dict[tuple[int, int], EventSubscriber] = None
    _logger: logging.Logger = None

    def __init__(self, logger: logging.Logger, subscribers: list[EventSubscriber] = None):
        """
        Constructor
        :param logger:
        """
        self._logger = logger
        if not subscribers:
            subscribers = []
        if not self._subscribers:
            self._subscribers = {}
        for subscriber in subscribers:
            self.register(subscriber)

    def register(self, subscriber: EventSubscriber, increment: int = 0) -> None:
        """
        Adds another subscriber to the set of subscribers handled by this class.
        :param subscriber:
        :param increment: Do not use this argument directly. Used internally to set the correct order of subscribers.
        :return:
        """
        if (subscriber.get_order(), increment) in self._subscribers:
            self.register(subscriber, increment + 1)
            return

        self._subscribers[(subscriber.get_order(), increment)] = subscriber
        return

    def dispatch(self, events: list[Enum], data: IsDataClass) -> None:
        """
        Dispatch one or more events. Runs all subscribers that are subscribed to one or more of the events.
        :param events: Any kind of Enum set to a specific value.
        :param data: Any kind of data expected by subscribers listening to it.
        """
        self._logger.debug(f'Dispatching “{", ".join(Utils.enums_to_iterable(events))}” events.')

        for subscriber in dict(sorted(self._subscribers.items())).values():
            subscribed_events: list[Enum] = list(set(events).intersection(subscriber.get_subscribed_events()))
            if len(subscribed_events) > 0:
                result = subscriber.run(data)
                if result not in [Status.SUCCESS, Status.NOT_RUN]:
                    self._logger.warning(
                        f'“{Utils.classname(subscriber)}” failed.'
                    )
                if result is Status.SUCCESS:
                    self._logger.debug(
                        f'“{Utils.classname(subscriber)}” was run in response to '
                        f'“{", ".join(Utils.enums_to_iterable(subscribed_events))}” events'
                    )
                if result is Status.NOT_RUN:
                    self._logger.debug(
                        f'“{Utils.classname(subscriber)}” was skipped.'
                    )
                if subscriber.must_stop_propagation():
                    self._logger.debug(f'Stopping event propagation as per “{Utils.classname(subscriber)}” option.')
                    break
