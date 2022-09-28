""" argument_reader.py test suit """
from unittest.mock import MagicMock

from wg_federation.input.reader.argument_reader import ArgumentReader


class TestArgumentReader:
    """ Test ArgumentReader class """

    _subject: ArgumentReader = None
    _program_version = '1.1.1'
    _argument_parser = MagicMock()
    _sub_argument_parser_action = MagicMock()
    _sub_argument_parser = MagicMock()

    def setup(self):
        """ Constructor """
        self._sub_argument_parser_action.add_parser = MagicMock(return_value=self._sub_argument_parser)
        self._argument_parser.add_subparsers = MagicMock(return_value=self._sub_argument_parser_action)
        self._argument_parser.parse_args = MagicMock(return_value='parse_result')

        self._subject = ArgumentReader(
            argument_parser=self._argument_parser,
            program_version=self._program_version
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ArgumentReader)

    def test_parse_all(self):
        """ it sets up all possible arguments and options and parses and returns the current argv """
        result = self._subject.parse_all()

        # pylint: disable=duplicate-code
        self._argument_parser.add_argument.assert_any_call(
            '-V',
            '--version',
            action='version',
            version=self._program_version,
            help='Shows the version number and exit.'
        )
        self._argument_parser.add_argument.was_called()
        self._argument_parser.add_subparsers.assert_called()
        self._argument_parser.add_parser.assert_not_called()
        self._sub_argument_parser_action.add_parser.assert_called()
        self._sub_argument_parser.add_argument.assert_called()

        assert 'parse_result' == result
