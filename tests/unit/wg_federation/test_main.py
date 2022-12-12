""" main.py test suit """
from unittest.mock import MagicMock

from wg_federation import Main
from wg_federation.controller.controller_events import ControllerEvents


class TestMain:
    """ Test Main class """

    _subject: Main = None
    _input_manager = MagicMock()
    _controller_dispatcher = MagicMock()
    _container = MagicMock()
    _user_input = MagicMock()

    def setup_method(self):
        """ Constructor """
        self._container.input_manager = MagicMock(return_value=self._input_manager)
        self._container.controller_dispatcher = MagicMock(return_value=self._controller_dispatcher)
        self._input_manager.parse_all = MagicMock(return_value=self._user_input)
        self._subject = Main(self._container)

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, Main)
        self._container.wire.assert_called()

    def test_main(self):
        """ it runs the main application """
        self._subject.main()
        self._input_manager.parse_all.assert_called_once()
        self._controller_dispatcher.dispatch.assert_called_once_with([
            ControllerEvents.CONTROLLER_BASELINE,
            ControllerEvents.CONTROLLER_MAIN,
            ControllerEvents.CONTROLLER_LATE,
        ], self._user_input)
