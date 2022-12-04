from wg_federation.controller.controller_interface import ControllerInterface
from wg_federation.controller.controller_status import Status
from wg_federation.data.input.user_input import UserInput
from wg_federation.state.manager.state_data_manager import StateDataManager


class StateHQBootstrapController(ControllerInterface):
    """
    Bootstrap HQ server.
    """

    _state_data_manager: StateDataManager = None

    def __init__(
            self,
            state_data_manager: StateDataManager
    ):
        """
        Constructor
        :param state_data_manager:
        """
        self._state_data_manager = state_data_manager

    def run(self, user_input: UserInput) -> Status:
        self._state_data_manager.create_hq_state()
        return Status.SUCCESS

    def should_run(self, user_input: UserInput) -> bool:
        return user_input.arg0 == 'hq' and user_input.arg1 == 'bootstrap'
