import os
from unittest.mock import patch, mock_open

import yaml

from wg_federation.data_transformation.loader.file.yaml_file_configuration_loader import YamlFileConfigurationLoader


class TestYamlFileConfigurationLoader:
    """ Test ConfigurationLoader class """

    _subject: YamlFileConfigurationLoader = None

    def setup_method(self):
        """ Constructor """

        self._subject = YamlFileConfigurationLoader()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, YamlFileConfigurationLoader)

    def test_get_supported_source(self):
        """ it returns its supported source """
        assert 'yaml_file' == self._subject.get_supported_source()

    def test_supports(self):
        """ it returns whether it supports a source or not """
        with patch.object(os.path, 'isfile', return_value=True):
            assert True is self._subject.supports('/path/to/file.yaml')
            assert True is self._subject.supports('/path/to/file.YAML')
            assert True is self._subject.supports('/path/to/file.yml')
            assert False is self._subject.supports('/path/to/file.json')
            assert False is self._subject.supports('yaml')

    def test_supports2(self):
        """ it returns it does not support an file that does not exist """
        with patch.object(os.path, 'isfile', return_value=False):
            assert False is self._subject.supports('/path/to/file.yaml')
            assert False is self._subject.supports('/path/to/file.YAML')
            assert False is self._subject.supports('/path/to/file.yml')

    def test_load_from(self):
        """ it can load configuration from a valid source """
        with patch('builtins.open', mock_open(read_data='data')):
            with patch.object(yaml, 'safe_load', return_value={'data_yaml': 1}) as yaml_load:
                result = self._subject.load_from('source')

        assert {'data_yaml': 1} == result
        yaml_load.assert_called_once()

    def test_load_from2(self):
        """ it can load configuration from a valid source, and makes sure to always a dict """
        with patch('builtins.open', mock_open(read_data='data')):
            with patch.object(yaml, 'safe_load', return_value='not_dict') as yaml_data:
                result = self._subject.load_from('source')

        assert {} == result
        yaml_data.assert_called_once()
