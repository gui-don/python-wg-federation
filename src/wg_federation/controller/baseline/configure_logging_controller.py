import logging
from wg_federation.controller.controller_interface import ControllerInterface
from wg_federation.controller.controller_status import Status
from wg_federation.data.input.user_input import UserInput


class ConfigureLoggingController(ControllerInterface):
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

    def run(self, user_input: UserInput) -> Status:
        if user_input.quiet:
            logging.disable()
            return Status.SUCCESS

        # This is a mask (as in POSIX permission mask): the Handler object sets the real logging level.
        self._logger.setLevel(logging.DEBUG)

        self._logger_handler.setLevel(logging.getLevelName(user_input.log_level))

        if user_input.verbose:
            self._logger_handler.setLevel(logging.INFO)

        if user_input.debug:
            self._logger_handler.setLevel(logging.DEBUG)

        return Status.SUCCESS

    def should_run(self, user_input: UserInput) -> bool:
        return True
