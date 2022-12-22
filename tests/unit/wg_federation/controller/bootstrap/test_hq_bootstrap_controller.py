from unittest.mock import MagicMock

import pytest
from mockito import unstub, mock, verify, verifyNoUnwantedInteractions

from wg_federation.controller.bootstrap.hq_bootstrap_controller import HQBootstrapController
from wg_federation.controller.controller_events import ControllerEvents
from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver
from wg_federation.data.input.user_input import UserInput
from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.state.manager.state_data_manager import StateDataManager


class TestHQBootstrapController:
    """ Test HQBootstrapController class """

    _user_input: UserInput = None
    _state_data_manager: StateDataManager = None
    _cryptographic_key_deriver: CryptographicKeyDeriver = None

    _subject: HQBootstrapController = None

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

        self._subject = HQBootstrapController(
            state_data_manager=self._state_data_manager,
            cryptographic_key_deriver=self._cryptographic_key_deriver,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, HQBootstrapController)
        assert isinstance(self._subject, EventSubscriber)

    def test_get_subscribed_events(self):
        """ it returns the events it is subscribed to """
        assert [ControllerEvents.CONTROLLER_MAIN] == self._subject.get_subscribed_events()

    def test_run1(self):
        """ it creates a new HQState """

        assert self._user_input == self._subject.run(self._user_input)

        verify(self._cryptographic_key_deriver, times=1).create_salt()
        verify(self._state_data_manager, times=1).create_hq_state(self._user_input)

        verifyNoUnwantedInteractions()

    def test_should_run(self):
        """ it does run if the arguments are 'hq bootstrap' """

        assert self._subject.should_run(self._user_input)

    def test_should_run1(self):
        """ it does not run if the arguments are not 'hq bootstrap' """

        self._user_input.arg0 = 'member'

        assert not self._subject.should_run(self._user_input)
