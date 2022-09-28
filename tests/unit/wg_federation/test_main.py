""" main.py test suit """
from unittest.mock import MagicMock

from wg_federation import Main


class TestMain:
    """ Test Main class """

    _subject: Main = None
    _input_manager = MagicMock()
    _container = MagicMock()
    _user_input = MagicMock()

    def setup(self):
        """ Constructor """
        self._input_manager.parse_all = MagicMock(return_value=self._user_input)
        self._subject = Main(self._container)

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, Main)
        self._container.wire.assert_called()

    def test_main(self):
        """ it runs the main application """
        self._subject.main(self._input_manager)
        assert self._user_input == self._container.user_input
