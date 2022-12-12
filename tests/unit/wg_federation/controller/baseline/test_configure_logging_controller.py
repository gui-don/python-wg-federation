""" configure_logging_controller.py test suit """
import logging
from unittest.mock import MagicMock

import pytest
from mockito import unstub, mock, verify, patch

from wg_federation.controller.baseline.configure_logging_controller import ConfigureLoggingController
from wg_federation.controller.controller_events import ControllerEvents
from wg_federation.data.input.log_level import LogLevel
from wg_federation.data.input.user_input import UserInput
from wg_federation.observer.status import Status


class TestConfigureLoggingController:
    """ Test ConfigureLoggingController class """

    _logger = None
    _logger_handler = None
    _user_input: UserInput = None
    _user_input_debug: UserInput = None
    _user_input_quiet: UserInput = None

    _subject: ConfigureLoggingController = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """

        self._logger_handler = mock()
        self._logger = mock()

        self._user_input_quiet = MagicMock(spec=UserInput)
        self._user_input_quiet.quiet = True

        self._user_input = MagicMock(spec=UserInput)
        self._user_input.quiet = False
        self._user_input.log_level = LogLevel.INFO
        self._user_input.verbose = True
        self._user_input.debug = False

        self._user_input_debug = MagicMock(spec=UserInput)
        self._user_input_debug.quiet = False
        self._user_input_debug.log_level = LogLevel.ERROR
        self._user_input_debug.verbose = False
        self._user_input_debug.debug = True

        self._subject = ConfigureLoggingController(
            logger_handler=self._logger_handler,
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ConfigureLoggingController)

    def test_get_subscribed_events(self):
        """ it returns the events it is subscribed to """
        assert [ControllerEvents.CONTROLLER_BASELINE] == self._subject.get_subscribed_events()

    def test_run1(self):
        """ it disables logging if user set the quiet flag """
        patch(logging.disable, lambda: None)

        result = self._subject.run(self._user_input_quiet)

        verify(self._logger, times=0).setLevel(logging.DEBUG)
        verify(logging, times=1).disable()
        assert Status.SUCCESS == result

    def test_run2(self):
        """ it does not disable logging if user did not set the quiet flag """
        patch(logging.disable, lambda: None)

        self._subject.run(self._user_input)

        verify(logging, times=0).disable()

    def test_run3(self):
        """ it sets logger level to INFO when if user set the verbose flag """

        result = self._subject.run(self._user_input)

        verify(self._logger, times=1).setLevel(logging.DEBUG)
        verify(self._logger_handler, times=2).setLevel(logging.INFO)
        assert Status.SUCCESS == result

    def test_run4(self):
        """ it sets logger level to DEBUG when if user set the debug flag """

        result = self._subject.run(self._user_input_debug)

        verify(self._logger, times=1).setLevel(logging.DEBUG)
        verify(self._logger_handler, times=1).setLevel(logging.DEBUG)

        assert Status.SUCCESS == result

    def test_run5(self):
        """ it sets logger level to the log level that user define, but may be overridden by other flags """
        result = self._subject.run(self._user_input_debug)

        verify(self._logger, times=1).setLevel(logging.DEBUG)
        verify(self._logger_handler, times=1).setLevel(logging.DEBUG)
        verify(self._logger_handler, times=1).setLevel(logging.ERROR)

        assert Status.SUCCESS == result

    def test_run6(self):
        """ it does not support running with data objects that are not UserInput """
        with pytest.raises(RuntimeError) as error:
            self._subject.run(self._logger)

        assert 'ConfigureLoggingController♦ responded to an event with unsupported data type “Dummy”.' in str(error)
