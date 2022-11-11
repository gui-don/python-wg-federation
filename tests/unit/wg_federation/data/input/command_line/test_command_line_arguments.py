from unittest.mock import MagicMock

from wg_federation.data.input.command_line.command_line_argument import CommandLineArgument
from wg_federation.data.input.command_line.command_line_option import CommandLineOption


class TestCommandLineArgument:
    """ Test CommandLineArgument class """

    _subject: CommandLineArgument = None

    _command_line_argument: CommandLineArgument = MagicMock()
    _command_line_option: CommandLineOption = MagicMock()

    def setup_method(self):
        """ Constructor """
        self._subject = CommandLineArgument(
            command='a_command',
            description='a_description'
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, CommandLineArgument)

    def test_data(self):
        """ it returns its data """
        assert 'a_command' == self._subject.command
        assert 'a_description' == self._subject.description
