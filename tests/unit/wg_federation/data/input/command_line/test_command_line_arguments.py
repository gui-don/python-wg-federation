import pytest
from mockito import unstub

from wg_federation.data.input.command_line.command_line_argument import CommandLineArgument
from wg_federation.data.input.command_line.command_line_option import CommandLineOption


class TestCommandLineArgument:
    """ Test CommandLineArgument class """

    _subject: CommandLineArgument = None

    _command_line_argument: CommandLineArgument = None
    _command_line_option: CommandLineOption = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """
        self._command_line_argument = CommandLineArgument(
            command='cmd',
            description='desc',
        )
        self._command_line_option = CommandLineOption(
            argument_alias='--alias',
            argument_short='-a',
            description='desc',
            name='test',
        )

        self._subject = CommandLineArgument(
            command='a_command',
            description='a_description',
            subcommands=[self._command_line_argument],
            options=[self._command_line_option],
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, CommandLineArgument)

    def test_data(self):
        """ it returns its data """
        assert 'a_command' == self._subject.command
        assert 'a_description' == self._subject.description
        assert self._command_line_argument == self._subject.subcommands[0]
        assert self._command_line_option == self._subject.options[0]
