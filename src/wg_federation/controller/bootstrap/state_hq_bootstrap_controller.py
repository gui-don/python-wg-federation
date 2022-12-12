from enum import Enum

from wg_federation.controller.controller import Controller
from wg_federation.controller.controller_events import ControllerEvents
from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver
from wg_federation.data.input.user_input import UserInput
from wg_federation.observer.status import Status
from wg_federation.state.manager.state_data_manager import StateDataManager


class StateHQBootstrapController(Controller):
    """
    Bootstrap HQ server.
    """

    _state_data_manager: StateDataManager = None
    _cryptographic_key_deriver: CryptographicKeyDeriver = None

    def __init__(
            self,
            state_data_manager: StateDataManager,
            cryptographic_key_deriver: CryptographicKeyDeriver,
    ):
        """
        Constructor
        :param state_data_manager:
        :param cryptographic_key_deriver:
        """
        self._state_data_manager = state_data_manager
        self._cryptographic_key_deriver = cryptographic_key_deriver

    def get_subscribed_events(self) -> list[Enum]:
        return [ControllerEvents.CONTROLLER_MAIN]

    # pylint: disable=unused-argument
    def _do_run(self, data: UserInput) -> Status:
        self._cryptographic_key_deriver.create_salt()

        self._state_data_manager.create_hq_state()
        return Status.SUCCESS

    def _should_run(self, data: UserInput) -> bool:
        return data.arg0 == 'hq' and data.arg1 == 'bootstrap'
