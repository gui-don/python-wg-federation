import json
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

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

    def test_load_from(self):
        """ it can load configuration from a valid source """
        with patch.object(Path, 'is_file', return_value=True):
            with patch('builtins.open', mock_open(read_data='data')):
                with patch.object(json, 'load', return_value='json_data') as json_data:
                    result = self._subject.load_from('source')

        assert 'json_data' == result
        json_data.assert_called_once()

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
                with patch.object(json, 'load', return_value='json_data') as json_data:
                    result = self._subject.load_from_all(('source1', 'source2'))

        assert 'json_data' == result
        json_data.assert_called()
