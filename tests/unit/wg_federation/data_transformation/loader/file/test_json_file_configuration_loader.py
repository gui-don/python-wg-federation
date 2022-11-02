import json
from pathlib import Path
from unittest.mock import patch, mock_open

from wg_federation.data_transformation.loader.file.json_file_configuration_loader import JsonFileConfigurationLoader


# Because this is a test of a template pattern classes.
# Therefore, it looks similar of any other test of the subclasses
# pylint: disable=duplicate-code
class TestJsonFileConfigurationLoader:
    """ Test ConfigurationLoader class """

    _subject: JsonFileConfigurationLoader = None

    def setup(self):
        """ Constructor """

        self._subject = JsonFileConfigurationLoader()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, JsonFileConfigurationLoader)

    def test_get_supported_source(self):
        """ it returns its supported source """
        assert 'json_file' == self._subject.get_supported_source()

    def test_supports(self):
        """ it returns whether it supports a source or not """
        with patch.object(Path, 'is_file', return_value=True):
            assert True is self._subject.supports('/path/to/file.json')
            assert True is self._subject.supports('file.json')
            assert False is self._subject.supports('/path/to/file.yml')
            assert False is self._subject.supports('.json')

    def test_supports2(self):
        """ it returns it does not support an file that does not exist """
        with patch.object(Path, 'is_file', return_value=False):
            assert False is self._subject.supports('/path/to/file.json')
            assert False is self._subject.supports('file.json')

    def test_load_from(self):
        """ it can load configuration from a valid source """
        with patch('builtins.open', mock_open(read_data='data')):
            with patch.object(json, 'load', return_value='json_data') as json_data:
                result = self._subject.load_from('source')

        assert 'json_data' == result
        json_data.assert_called_once()
