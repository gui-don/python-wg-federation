from pathlib import Path
from unittest.mock import patch, mock_open

import pytest
import yaml

from wg_federation.data_transformation.loader.file.yaml_file_configuration_loader import YamlFileConfigurationLoader


# Because this is a test of a template pattern classes.
# Therefore, it looks similar of any other test of the subclasses
# pylint: disable=duplicate-code
class TestYamlFileConfigurationLoader:
    """ Test ConfigurationLoader class """

    _subject: YamlFileConfigurationLoader = None

    def setup(self):
        """ Constructor """

        self._subject = YamlFileConfigurationLoader()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, YamlFileConfigurationLoader)

    def test_get_supported_source(self):
        """ it returns its supported source """
        assert 'yaml_file' == self._subject.get_supported_source()

    def test_load_from(self):
        """ it can load configuration from a valid source """
        with patch.object(Path, 'is_file', return_value=True):
            with patch('builtins.open', mock_open(read_data='data')):
                with patch.object(yaml, 'safe_load', return_value='data_yaml') as yaml_load:
                    result = self._subject.load_from('source')

        assert 'data_yaml' == result
        yaml_load.assert_called_once()

    def test_load_from2(self):
        """ it raises an error if source is not a file """

        with patch.object(Path, 'is_file', return_value=False):
            with pytest.raises(RuntimeError) as error:
                self._subject.load_from('source')

        assert 'The file does not exist' in str(error)

    def test_load_from_all(self):
        """ it can load multiple sources and deep merge them together into a configuration """

        with patch.object(Path, 'is_file', return_value=True):
            with patch('builtins.open', mock_open(read_data='data')):
                with patch.object(yaml, 'safe_load', return_value='data_yaml') as yaml_load:
                    result = self._subject.load_from_all(('source1', 'source2'))

        assert 'data_yaml' == result
        yaml_load.assert_called()
