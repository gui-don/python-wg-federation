import json
import os
from unittest.mock import patch, mock_open

from wg_federation.data_transformation.loader.file.json_file_configuration_loader import JsonFileConfigurationLoader


class TestJsonFileConfigurationLoader:
    """ Test JsonFileConfigurationLoader class """

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
        with patch.object(os.path, 'isfile', return_value=True):
            assert True is self._subject.supports('/path/to/file.json')
            assert True is self._subject.supports('file.json')
            assert False is self._subject.supports('/path/to/file.yml')
            assert False is self._subject.supports('.json')

    def test_supports2(self):
        """ it returns it does not support an file that does not exist """
        with patch.object(os.path, 'isfile', return_value=False):
            assert False is self._subject.supports('/path/to/file.json')
            assert False is self._subject.supports('file.json')

    def test_load_from(self):
        """ it can load configuration from a valid source """
        with patch('builtins.open', mock_open(read_data='data')):
            with patch.object(json, 'load', return_value={'json_data': 1}) as json_data:
                result = self._subject.load_from('source')

        assert {'json_data': 1} == result
        json_data.assert_called_once()

    def test_load_from2(self):
        """ it can load configuration from a valid source, and makes sure to always a dict """
        with patch('builtins.open', mock_open(read_data='data')):
            with patch.object(json, 'load', return_value='not_dict') as json_data:
                result = self._subject.load_from('source')

        assert {} == result
        json_data.assert_called_once()
