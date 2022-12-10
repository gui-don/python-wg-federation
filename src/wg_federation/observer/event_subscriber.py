from abc import ABC
from enum import Enum

from wg_federation.observer.is_data_class import IsDataClass
from wg_federation.observer.status import Status
from wg_federation.utils.utils import Utils


class EventSubscriber(ABC):
    """
    Abstract class for any kind of EventSubscriber any kind of events, previously registered.
    """

    def get_subscribed_events(self) -> list[Enum]:
        """
        Returns the list of events that this subscriber listens to
        :return:
        """

    def run(self, data: IsDataClass) -> Status:
        """
        Runs the subscriber after checking if data is valid
        :param data: Any kind of data expected by your specific implementation of a subscriber.
        :raise RuntimeError when data is not of the type returned by `support_data_class()`
        :return:
        """
        if not isinstance(data, self.support_data_class()):
            raise RuntimeError(
                f'{Utils.classname(self)} responded to an event with unsupported data type “{type(data).__name__}”.',
                f'Supported data type: “{self.support_data_class().__name__}”.'
            )

        return self._do_run(data)

    def _do_run(self, data: IsDataClass) -> Status:
        """
        Run the subscriber
        :param data:
        :return:
        """

    @classmethod
    def support_data_class(cls) -> type:
        """
        Returns what kind of data class this class supports
        :return:
        """

    @classmethod
    def must_stop_propagation(cls) -> bool:
        """
        Whether to stop propagation to other subscribers at the end of this specific subscriber.
        Useful when a specific subscriber requires preventing any other subscriber to run.
        :return:
        """
        return False

    @classmethod
    def get_order(cls) -> int:
        """
        Order of execution for this specific subscriber, compared to other subscribers.
        Lower values will always be executed before high values.
        Two subscribers with the same order value will have precedences determined by order of registration using FIFO.
        :return:
        """
        return 500
