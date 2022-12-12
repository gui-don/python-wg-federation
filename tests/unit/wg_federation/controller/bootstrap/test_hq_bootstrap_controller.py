from unittest.mock import MagicMock

import pytest
from mockito import unstub, mock, verify, verifyNoUnwantedInteractions

from wg_federation.controller.bootstrap.state_hq_bootstrap_controller import StateHQBootstrapController
from wg_federation.controller.controller import Controller
from wg_federation.controller.controller_events import ControllerEvents
from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver
from wg_federation.data.input.user_input import UserInput
from wg_federation.observer.status import Status
from wg_federation.state.manager.state_data_manager import StateDataManager


class TestStateHQBootstrapController:
    """ Test StateHQBootstrapController class """

    _user_input: UserInput = None
    _state_data_manager: StateDataManager = None
    _cryptographic_key_deriver: CryptographicKeyDeriver = None

    _subject: StateHQBootstrapController = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._user_input = MagicMock(spec=UserInput)
        self._user_input.arg0 = 'hq'
        self._user_input.arg1 = 'bootstrap'

        self._state_data_manager = mock()
        self._cryptographic_key_deriver = mock()

        self._subject = StateHQBootstrapController(
            state_data_manager=self._state_data_manager,
            cryptographic_key_deriver=self._cryptographic_key_deriver,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, StateHQBootstrapController)
        assert isinstance(self._subject, Controller)

    def test_get_subscribed_events(self):
        """ it returns the events it is subscribed to """
        assert [ControllerEvents.CONTROLLER_MAIN] == self._subject.get_subscribed_events()

    def test_run1(self):
        """ it creates a new HQState """

        assert Status.SUCCESS == self._subject.run(self._user_input)

        verify(self._cryptographic_key_deriver, times=1).create_salt()
        verify(self._state_data_manager, times=1).create_hq_state()

        verifyNoUnwantedInteractions()

    def test_run2(self):
        """ it does not run if the arguments are not 'hq bootstrap' """

        self._user_input.arg0 = 'member'

        assert Status.NOT_RUN == self._subject.run(self._user_input)

        verify(self._cryptographic_key_deriver, times=0).create_salt()
        verify(self._state_data_manager, times=0).create_hq_state()

        verifyNoUnwantedInteractions()
