""" argument_reader.py test suit """

import pytest
from mockito import unstub, contains, when, mock, verify

from wg_federation.input.reader.argument_reader import ArgumentReader


class TestArgumentReader:
    """ Test ArgumentReader class """

    _subject: ArgumentReader = None
    _program_version = '1.1.1'
    _argument_parser = None
    _sub_argument_parser_action = None
    _sub_argument_parser = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """

        self._sub_argument_parser = mock()

        self._sub_argument_parser_action = mock()
        when(self._sub_argument_parser_action).add_parser(...).thenReturn(self._sub_argument_parser)
        when(self._sub_argument_parser).add_subparsers(...).thenReturn(self._sub_argument_parser_action)

        self._argument_parser = mock()
        when(self._argument_parser).add_subparsers(
            required=False, dest=contains('arg')
        ).thenReturn(self._sub_argument_parser_action)
        when(self._argument_parser).parse_args().thenReturn('parse_result')

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
        verify(self._argument_parser, times=9).add_argument(...)
        verify(self._argument_parser, times=1).add_argument(
            '-V',
            '--version',
            action='version',
            version=self._program_version,
            help='Shows the version number and exit.'
        )
        verify(self._sub_argument_parser, atleast=1).add_argument(...)
        verify(self._argument_parser, times=1).parse_args()

        assert 'parse_result' == result
