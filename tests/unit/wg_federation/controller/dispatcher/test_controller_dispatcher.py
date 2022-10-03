""" controller_dispatcher.py test suit """
from unittest.mock import MagicMock

import pytest

from wg_federation.controller.dispatcher.controller_dispatcher import ControllerDispatcher
from wg_federation.controller.dispatcher.controller_status import Status


class TestControllerDispatcher:
    """ Test ControllerDispatcher class """

    _controller1 = MagicMock()
    _controller2 = MagicMock()
    _controller3 = MagicMock()
    _controller4 = MagicMock()
    _logger = MagicMock()
    _user_input = MagicMock()

    _subject: ControllerDispatcher = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mocks between tests """
        self._logger.reset_mock()

    def setup(self):
        """ Constructor """

        self._controller1.should_run = MagicMock(return_value=True)
        self._controller1.run = MagicMock(return_value=Status.SUCCESS)

        self._controller2.should_run = MagicMock(return_value=False)

        self._controller3.should_run = MagicMock(return_value=True)
        self._controller3.run = MagicMock(return_value=Status.SUCCESS)

        self._controller4.run = MagicMock(return_value=Status.DEFAULT_ERROR)

        self._subject = ControllerDispatcher(
            controllers=[
                self._controller1, self._controller2, self._controller3
            ],
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ControllerDispatcher)

    def test_enroll1(self):
        """ it enrolls new controllers """
        self._subject.enroll(self._controller4)

    def test_enroll2(self):
        """ it raises an exception when trying to enroll an already-enrolled controller """
        with pytest.raises(RuntimeError):
            self._subject.enroll(self._controller3)

    def test_dispatch_all1(self):
        """ it dispatches all the controllers in order """
        self._subject.dispatch_all(self._user_input)

        self._controller1.run.assert_called_once_with(self._user_input)
        self._controller2.run.assert_not_called()
        self._controller3.run.assert_called_once_with(self._user_input)

    def test_dispatch_all2(self):
        """ it raises an Exception when one of the controller fails """
        self._subject.enroll(self._controller4)

        with pytest.raises(RuntimeError):
            self._subject.dispatch_all(self._user_input)

        self._controller4.run.assert_called_once_with(self._user_input)
