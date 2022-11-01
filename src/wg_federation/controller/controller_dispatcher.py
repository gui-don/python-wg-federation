import logging

from wg_federation.controller.controller_interface import ControllerInterface
from wg_federation.controller.controller_status import Status
from wg_federation.data.input.user_input import UserInput


class ControllerDispatcher:
    """
    Enroll ControllerInterface objects and dispatch them when needed.
    """
    _controllers: tuple[ControllerInterface, ...] = None
    _logger: logging.Logger = None

    def __init__(
            self,
            controllers: tuple[ControllerInterface, ...],
            logger: logging.Logger,
    ):
        """
        Constructor
        :param controllers: careful, order is very important. Object first in the list will be run first.
        :param logger:
        """
        self._controllers = tuple(controllers)
        self._logger = logger

    def dispatch_all(self, user_input: UserInput) -> None:
        """
        Runs all supported controller, depending on user inputs
        :param user_input: all user defined inputs
        :raise RuntimeError: when a controller return a non-successful status
        """
        for controller in self._controllers:
            if controller.should_run(user_input):
                result = controller.run(user_input)

                if Status.SUCCESS != result:
                    raise RuntimeError(f'{controller.__class__} failed with status code {result}')

                self._logger.debug(f'{controller.__class__} was run.')
            else:
                self._logger.debug(f'{controller.__class__} was queued to run, but it did not in current context.')

    def enroll(self, controller: ControllerInterface) -> None:
        """
        Enroll a controller to the list of available controller.
        Careful, newly enrolled controllers will always be run after all existing controllers.
        :param controller: the controller to enroll
        :raise RuntimeError: when controller was already enrolled
        """
        self.__enroll_check(controller)

        self._controllers += (controller,)

    def __enroll_check(self, controller: ControllerInterface) -> None:
        if controller in self._controllers:
            raise RuntimeError(f'{controller.__class__} was enrolled twice. This can lead to performance issues.')
