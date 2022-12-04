import pytest
from mockito import unstub, mock, verify, verifyNoUnwantedInteractions

from wg_federation.controller.bootstrap.state_hq_bootstrap_controller import StateHQBootstrapController
from wg_federation.controller.controller_interface import ControllerInterface
from wg_federation.controller.controller_status import Status


class TestStateHQBootstrapController:
    """ Test StateHQBootstrapController class """

    _user_input = None
    _state_data_manager = None

    _subject: StateHQBootstrapController = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """
        self._user_input = mock({'arg0': 'hq', 'arg1': 'bootstrap'})

        self._state_data_manager = mock()

        self._subject = StateHQBootstrapController(
            state_data_manager=self._state_data_manager,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, StateHQBootstrapController)
        assert isinstance(self._subject, ControllerInterface)

    def test_should_run(self):
        """ it checks whether it should run """
        assert self._subject.should_run(self._user_input)

        _user_input = mock({'arg0': 'hq', 'arg1': 'not'})
        assert not self._subject.should_run(_user_input)

        _user_input = mock({'arg0': 'not', 'arg1': 'bootstrap'})
        assert not self._subject.should_run(_user_input)

    def test_run1(self):
        """ it creates a new HQState """

        assert Status.SUCCESS == self._subject.run(self._user_input)

        verify(self._state_data_manager, times=1).create_hq_state()

        verifyNoUnwantedInteractions()
