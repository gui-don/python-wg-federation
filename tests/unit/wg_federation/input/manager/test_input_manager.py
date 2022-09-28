""" input_manager.py test suit """
from unittest.mock import MagicMock

from wg_federation.input.data.user_input import UserInput
from wg_federation.input.manager.input_manager import InputManager


class Struct:
    """ Helps to convert a dict into an object for testing purpose """

    def __init__(self, **entries):
        self.__dict__.update(entries)


class TestInputManager:
    """ Test InputManager class """

    _logger = MagicMock()
    _environment_variable_reader = MagicMock()
    _argument_reader = MagicMock()
    _subject: InputManager = None

    def setup(self):
        """ Constructor """
        self._environment_variable_reader.fetch_all = MagicMock(return_value={'debug': 'True'})
        self._argument_reader.parse_all = MagicMock(return_value=Struct(**{'verbose': True, 'arg0': 'test'}))
        self._subject = InputManager(
            argument_reader=self._argument_reader,
            environment_variable_reader=self._environment_variable_reader,
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, InputManager)

    def test_parse_all(self):
        """ it parses all possible sources and returns and returns a data object of the result """
        result = self._subject.parse_all()

        self._logger.debug.assert_called()
        self._argument_reader.parse_all.assert_called()
        self._environment_variable_reader.fetch_all.assert_called()
        assert isinstance(result, UserInput)
        assert True is result.verbose
        assert True is result.debug
        assert False is result.quiet
        assert 'test' == result.arg0
