import logging
from enum import Enum

from wg_federation.controller.controller import Controller
from wg_federation.controller.controller_events import ControllerEvents
from wg_federation.data.input.user_input import UserInput
from wg_federation.observer.status import Status


class ConfigureLoggingController(Controller):
    """
    Configure the application logging
    For example, logging level depending on user inputs

    Note: this code can be run quite late during the flow of the program.
    To enable debug sooner, see the dependency injection Container class.
    """
    _logger_handler: logging.Handler = None
    _logger: logging.Logger = None

    def __init__(self, logger_handler: logging.Handler, logger: logging.Logger):
        """
        Constructor
        :param logger_handler:
        :param logger:
        """
        self._logger_handler = logger_handler
        self._logger = logger

    def get_subscribed_events(self) -> list[Enum]:
        return [ControllerEvents.CONTROLLER_BASELINE]

    def _do_run(self, data: UserInput) -> Status:
        if data.quiet:
            logging.disable()
            return Status.SUCCESS

        # This is a mask (as in POSIX permission mask): the Handler object sets the real logging level.
        self._logger.setLevel(logging.DEBUG)
        self._logger_handler.setLevel(logging.getLevelName(data.log_level))

        if data.verbose:
            self._logger_handler.setLevel(logging.INFO)

        if data.debug:
            self._logger_handler.setLevel(logging.DEBUG)

        return Status.SUCCESS

    def _should_run(self, data: UserInput) -> bool:
        return True
