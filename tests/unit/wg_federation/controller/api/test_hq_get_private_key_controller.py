import os
from unittest.mock import MagicMock

import pytest
from mockito import unstub, mock, when, verify, verifyNoUnwantedInteractions

from unit.wg_federation import hq_state
from wg_federation.controller.api.hq_get_private_key_controller import HQGetPrivateKeyController
from wg_federation.controller.controller_events import ControllerEvents
from wg_federation.data.input.user_input import UserInput
from wg_federation.data.state.hq_state import HQState
from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.state.manager.state_data_manager import StateDataManager


class TestHQGetPrivateKeyController:
    """ Test HQGetPrivateKeyController class """

    _user_input: UserInput = None
    _hq_state: HQState = None
    _state_data_manager: StateDataManager = None

    _subject: HQGetPrivateKeyController = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """
        self._hq_state = hq_state()

        self._user_input = MagicMock(spec=UserInput)
        self._user_input.arg0 = 'hq'
        self._user_input.arg1 = 'get-private-key'
        self._user_input.interface_kind = 'forums'
        self._user_input.interface_name = 'forum0'

        self._state_data_manager = mock()
        when(self._state_data_manager).reload().thenReturn(self._hq_state)

        self._subject = HQGetPrivateKeyController(
            state_data_manager=self._state_data_manager,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, HQGetPrivateKeyController)
        assert isinstance(self._subject, EventSubscriber)

    def test_get_subscribed_events(self):
        """ it returns the events it is subscribed to """
        assert [ControllerEvents.CONTROLLER_MAIN] == self._subject.get_subscribed_events()

    def test_run1(self, capfd):
        """ it returns a private key """

        assert self._user_input == self._subject.run(self._user_input)

        verify(self._state_data_manager, times=1).reload()
        assert capfd.readouterr()[0] == 'GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=' + os.linesep
        verifyNoUnwantedInteractions()

    def test_run2(self, capfd):
        """ it does not return anything if the given interface name or kind does not exist """
        self._user_input.interface_kind = 'nope'

        assert self._user_input == self._subject.run(self._user_input)

        self._user_input.interface_kind = 'forums'
        self._user_input.interface_name = 'does_not_exists'

        assert self._user_input == self._subject.run(self._user_input)

        verify(self._state_data_manager, times=2).reload()
        assert capfd.readouterr()[0] == ''
        verifyNoUnwantedInteractions()

    def test_should_run1(self):
        """ it does run if the arguments are 'hq get-private-key' """

        assert self._subject.should_run(self._user_input)

    def test_should_run2(self):
        """ it does not run if the arguments are not 'hq get-private-key' """

        self._user_input.arg1 = 'bootstrap'

        assert not self._subject.should_run(self._user_input)
