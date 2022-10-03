from abc import ABC, abstractmethod
from wg_federation.controller.dispatcher.controller_status import Status
from wg_federation.input.data.user_input import UserInput


class ControllerInterface(ABC):
    """
    Controller interface. Represents any controller
    """

    @abstractmethod
    def run(self, user_input: UserInput) -> Status:
        """
        Run the controller actions
        :param user_input: user inputs
        :return: status of the controller
        """

    @abstractmethod
    def should_run(self, user_input: UserInput) -> bool:
        """
        Whether the controller should be run
        :param user_input: user inputs
        :return: True if this controller should be run, False otherwise
        """
