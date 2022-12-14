from wg_federation.data.input.command_line.argparse_action import ArgparseAction
from wg_federation.data.input.command_line.command_line_option import CommandLineOption


class TestCommandLineOption:
    """ Test CommandLineOption class """

    _subject: CommandLineOption = None

    def setup(self):
        """ Constructor """
        self._subject = CommandLineOption(
            argparse_action=ArgparseAction.STORE,
            argument_alias='an_alias',
            argument_short='a_short',
            default='a_default',
            description='a_description',
            name='a_name',
            type=str,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, CommandLineOption)

    def test_data(self):
        """ it returns its data """
        assert ArgparseAction.STORE is self._subject.argparse_action
        assert 'an_alias' == self._subject.argument_alias
        assert 'a_short' == self._subject.argument_short
        assert 'a_default' == self._subject.default
        assert 'a_description' == self._subject.description
        assert 'a_name' == self._subject.name
        assert str is self._subject.type
