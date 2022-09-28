""" environment_variable_reader.py test suit """
from unittest.mock import MagicMock, patch

from wg_federation.input.reader.environment_variable_reader import EnvironmentVariableReader


class TestEnvironmentVariableReader:
    """ Test EnvironmentVariableReader class """

    _subject: EnvironmentVariableReader = None
    _logger = MagicMock()

    def setup(self):
        """ Constructor """
        self._subject = EnvironmentVariableReader(
            logger=self._logger,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, EnvironmentVariableReader)

    @patch.dict('os.environ', {'WG_FEDERATION_DEBUG': 'True'})
    def test_fetch_all(self):
        """ it reads all environment variables for each possible options """
        result = self._subject.fetch_all()

        self._logger.debug.assert_called()
        assert 'True' == result.get('debug')
        assert 'quiet' in result
        assert 'verbose' in result

    @patch.dict('os.environ', {'WG_FEDERATION_TEST': 'test'})
    def test_read(self):
        """ it reads an environment variable from the current system context """
        result = self._subject.read('TEST')

        self._logger.debug.assert_called()
        assert 'test' == result

    def test_read2(self):
        """ it returns None if an environment variable does not exist in the context """
        result = self._subject.read('TEST')

        assert None is result

    def test_get_real_env_var_name(self):
        """ it returns the real environment variable name from a suffix """
        assert 'WG_FEDERATION_TEST' == EnvironmentVariableReader.get_real_env_var_name('test')

    def test_get_all_options_env_var_names(self):
        """ it returns all possible environment variables real names for command line options """
        assert 'WG_FEDERATION_VERBOSE' in EnvironmentVariableReader.get_all_options_env_var_names()
        assert 'WG_FEDERATION_QUIET' in EnvironmentVariableReader.get_all_options_env_var_names()
