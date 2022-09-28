""" Main class """

from dependency_injector.wiring import Provide, inject

from wg_federation.di.container import Container
from wg_federation.input.manager.input_manager import InputManager


class Main:
    """ Main """

    _container: Container = None

    def __init__(self, container: Container = Container()):
        """
        Constructor
        """
        if self._container is None:
            self._container = container

        self._container.wire(modules=[__name__])

    @inject
    def main(
            self,
            input_manager: InputManager = Provide[Container.input_manager],
    ) -> int:
        """ main """

        self._container.user_input = input_manager.parse_all()
        self._container.wire(modules=[__name__], packages=['wg_federation.input.reader'])

        return 0
