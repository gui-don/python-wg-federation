""" configure_logging_controller.py test suit """
import logging
from unittest.mock import MagicMock, patch

import pytest

from wg_federation.controller.baseline.configure_logging_controller import ConfigureLoggingController
from wg_federation.controller.controller_status import Status
from wg_federation.data.input.log_level import LogLevel


class TestConfigureLoggingController:
    """ Test ConfigureLoggingController class """

    _logger = MagicMock()
    _logger_handler = MagicMock()
    _user_input = MagicMock()
    _user_input_debug = MagicMock()
    _user_input_quiet = MagicMock()

    _subject: ConfigureLoggingController = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        self._logger.reset_mock()
        self._logger_handler.reset_mock()

    def setup(self):
        """ Constructor """
        self._user_input_quiet.quiet = True

        self._user_input.quiet = False
        self._user_input.log_level = LogLevel.INFO
        self._user_input.verbose = True
        self._user_input.debug = False

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

    def test_should_run(self):
        """ it checks whether it should run """
        assert True is self._subject.should_run(self._user_input)

    def test_run1(self):
        """ it disables logging if user set the quiet flag """

        with patch.object(logging, 'disable', return_value=None) as logging_disabled:
            result = self._subject.run(user_input=self._user_input_quiet)

        logging_disabled.assert_called_once()
        self._logger.setLevel.assert_not_called()
        self._logger_handler.setLevel.assert_not_called()
        assert Status.SUCCESS == result

    def test_run2(self):
        """ it does not disable logging if user did not set the quiet flag """

        with patch.object(logging, 'disable', return_value=None) as logging_disabled:
            self._subject.run(user_input=self._user_input)

        logging_disabled.assert_not_called()

    def test_run3(self):
        """ it sets logger level to INFO when if user set the verbose flag """

        result = self._subject.run(user_input=self._user_input)

        self._logger.setLevel.assert_called_with(logging.DEBUG)
        self._logger_handler.setLevel.assert_called_with(logging.INFO)
        assert Status.SUCCESS == result

    def test_run4(self):
        """ it sets logger level to DEBUG when if user set the debug flag """

        result = self._subject.run(user_input=self._user_input_debug)

        self._logger.setLevel.assert_called_with(logging.DEBUG)
        self._logger_handler.setLevel.assert_called_with(logging.DEBUG)
        assert Status.SUCCESS == result

    def test_run5(self):
        """ it sets logger level to the log level that user define, but may be overridden by other flags """
        with patch.object(logging, 'getLevelName', return_value=logging.ERROR) as logging_get_level:
            result = self._subject.run(user_input=self._user_input_debug)

        logging_get_level.assert_called_once_with(LogLevel.ERROR)
        self._logger_handler.setLevel.assert_called_with(logging.DEBUG)
        self._logger_handler.setLevel.assert_any_call(logging.ERROR)
        assert Status.SUCCESS == result
