""" controller_dispatcher.py test suit """
from unittest.mock import MagicMock

import pytest

from wg_federation.controller.dispatcher.controller_dispatcher import ControllerDispatcher
from wg_federation.controller.dispatcher.controller_status import Status


class TestControllerDispatcher:
    """ Test ControllerDispatcher class """

    _working_controller = MagicMock()
    _not_run_controller = MagicMock()
    _working_controller_controller2 = MagicMock()
    _error_raised_controller = MagicMock()
    _logger = MagicMock()
    _user_input = MagicMock()

    _subject: ControllerDispatcher = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mocks between tests """
        self._logger.reset_mock()

    def setup(self):
        """ Constructor """

        self._working_controller.should_run = MagicMock(return_value=True)
        self._working_controller.run = MagicMock(return_value=Status.SUCCESS)

        self._not_run_controller.should_run = MagicMock(return_value=False)

        self._working_controller_controller2.should_run = MagicMock(return_value=True)
        self._working_controller_controller2.run = MagicMock(return_value=Status.SUCCESS)

        self._error_raised_controller.run = MagicMock(return_value=Status.DEFAULT_ERROR)

        self._subject = ControllerDispatcher(
            controllers=[
                self._working_controller, self._not_run_controller, self._working_controller_controller2
            ],
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ControllerDispatcher)

    def test_enroll1(self):
        """ it enrolls new controllers """
        self._subject.enroll(self._error_raised_controller)

    def test_enroll2(self):
        """ it raises an exception when trying to enroll an already-enrolled controller """
        with pytest.raises(RuntimeError):
            self._subject.enroll(self._working_controller_controller2)

    def test_dispatch_all1(self):
        """ it dispatches all the controllers in order """
        self._subject.dispatch_all(self._user_input)

        self._working_controller.run.assert_called_once_with(self._user_input)
        self._not_run_controller.run.assert_not_called()
        self._working_controller_controller2.run.assert_called_once_with(self._user_input)

    def test_dispatch_all2(self):
        """ it raises an Exception when one of the controller fails """
        self._subject.enroll(self._error_raised_controller)

        with pytest.raises(RuntimeError):
            self._subject.dispatch_all(self._user_input)

        self._error_raised_controller.run.assert_called_once_with(self._user_input)
