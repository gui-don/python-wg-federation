from unittest.mock import MagicMock

import pytest
from mockito import unstub

from wg_federation.controller.controller import Controller
from wg_federation.data.input.user_input import UserInput
from wg_federation.observer.status import Status


class DummyController(Controller):
    """ Dummy controller for tests """
    _should_run_data: bool = None
    _do_run_data: Status = None

    def __init__(self, should_run: bool, do_run: Status):
        self._should_run_data = should_run
        self._do_run_data = do_run

    # pylint: disable=unused-argument
    def _do_run(self, data: UserInput) -> Status:
        return self._do_run_data

    # pylint: disable=unused-argument
    def _should_run(self, data: UserInput) -> bool:
        return self._should_run_data


class TestController:
    """ Test Controller class """

    _user_input: UserInput = None

    _subject: Controller = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """
        self._user_input = MagicMock(spec=UserInput)

        self._subject = DummyController(True, Status.SUCCESS)

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, DummyController)
        assert isinstance(self._subject, Controller)

    def test_support_data_class(self):
        """ it returns what data class it supports """
        assert UserInput == self._subject.support_data_class()

    def test_run1(self):
        """ it runs """

        assert Status.SUCCESS == self._subject.run(self._user_input)

    def test_run2(self):
        """ it raise an error when run fails. """

        with pytest.raises(RuntimeError) as error:
            DummyController(True, Status.DEFAULT_ERROR).run(self._user_input)

        assert 'failed with status code' in str(error)
