""" Main class """
from wg_federation.controller.controller_dispatcher import ControllerDispatcher
from wg_federation.di.container import Container
from wg_federation.input.manager.input_manager import InputManager


class Main:
    """ Main """

    _container: Container = None

    def __init__(self, container: Container = None):
        """
        Constructor
        """
        if self._container is None:
            self._container = container or Container()

        self._container.wire(modules=[__name__])

    def main(self) -> int:
        """ main """
        input_manager: InputManager = self._container.input_manager()
        user_input = input_manager.parse_all()
        self._container.user_input.override(user_input)

        controller_dispatcher: ControllerDispatcher = self._container.controller_dispatcher()

        controller_dispatcher.dispatch_all(user_input)

        return 0
