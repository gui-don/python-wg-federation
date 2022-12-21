import subprocess

import pytest
from mockito import unstub, mock, when, verify, patch, contains

from wg_federation.data.input.user_input import UserInput
from wg_federation.input.manager.input_manager import InputManager


class Struct:
    """ Helps to convert a dict into an object for testing purpose """

    def __init__(self, **entries):
        self.__dict__.update(entries)


class TestInputManager:
    """ Test InputManager class """

    _command_result = None

    _logger = None
    _environment_variable_reader = None
    _argument_reader = None
    _configuration_file_reader = None
    _subject: InputManager = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """

        self._command_result = mock({''})

        self._logger = mock()

        self._environment_variable_reader = mock()
        when(self._environment_variable_reader).fetch_all().thenReturn({'debug': 'True'})

        self._argument_reader = mock()
        when(self._argument_reader).parse_all().thenReturn(Struct(**{'verbose': True, 'arg0': 'cmd'}))

        self._configuration_file_reader = mock()
        when(self._configuration_file_reader).load_all().thenReturn({'root_passphrase': 'test'})

        self._subject: InputManager = None

        self._subject = InputManager(
            argument_reader=self._argument_reader,
            environment_variable_reader=self._environment_variable_reader,
            configuration_file_reader=self._configuration_file_reader,
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, InputManager)

    def test_parse_all(self):
        """ it parses all possible sources and returns and returns a data object of the result """
        result = self._subject.parse_all()

        verify(self._argument_reader, times=1).parse_all()
        verify(self._environment_variable_reader, times=1).fetch_all()
        verify(self._configuration_file_reader, times=1).load_all()

        assert isinstance(result, UserInput)
        assert True is result.verbose
        assert True is result.debug
        assert False is result.quiet
        assert 'cmd' == result.arg0
        assert 'test' == result.root_passphrase.get_secret_value()

    def test_parse_all2(self):
        """ it processes the root passphrase through a subcommand """
        when(self._configuration_file_reader).load_all().thenReturn({'root_passphrase_command': 'test'})

        patch(subprocess.run, lambda *args, **kwargs: mock({'stdout': b'cmd result\n', 'returncode': 0}))

        result = self._subject.parse_all()
        assert 'cmd result' == result.root_passphrase.get_secret_value()

    def test_parse_all3(self):
        """ it raises an error when root passphrase subcommand returns a 'not 0' status """
        when(self._configuration_file_reader).load_all().thenReturn({'root_passphrase_command': 'test'})
        patch(subprocess.run, lambda *args, **kwargs: mock({'stdout': b'cmd result\n', 'returncode': 1}))

        with pytest.raises(ChildProcessError) as error:
            self._subject.parse_all()

        assert 'The command to get the root passphrase' in str(error)

    def test_parse_all4(self):
        """ it ignores root passphrase subcommand when root passphrase is defined from other means """
        when(self._environment_variable_reader).fetch_all().thenReturn({'root_passphrase_command': 'test'})
        patch(subprocess.run, lambda *args, **kwargs: mock({'stdout': b'cmd result\n', 'returncode': 0}))

        result = self._subject.parse_all()

        verify(self._logger, times=1).warning(contains('but the root passphrase was retrieved through other means.'))

        assert 'test' == result.root_passphrase.get_secret_value()

    def test_parse_all5(self):
        """ it warns if the root passphrase is within a configuration file """
        when(self._configuration_file_reader).load_all().thenReturn({'root_passphrase': 'test'})

        result = self._subject.parse_all()

        verify(self._logger, times=1).warning(
            contains('The secret “root_passphrase” was loaded from a configuration file.')
        )

        assert 'test' == result.root_passphrase.get_secret_value()
