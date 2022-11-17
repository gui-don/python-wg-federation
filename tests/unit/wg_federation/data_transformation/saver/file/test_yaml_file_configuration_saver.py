import builtins
import os
from io import TextIOWrapper
from unittest.mock import patch

import pytest
import yaml
from mockito import when, mock, unstub, ANY, verify, kwargs

from wg_federation.data_transformation.saver.file.yaml_file_configuration_saver import YamlFileConfigurationSaver


class TestYamlFileConfigurationSaver:
    """ Test YamlFileConfigurationSaver class """

    _file = None
    _subject: YamlFileConfigurationSaver = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._file = mock({'name': 'test.yaml'}, spec=TextIOWrapper)
        # pylint: disable=unnecessary-dunder-call
        when(self._file).__enter__(...).thenReturn(self._file)
        when(self._file).__exit__(...).thenReturn(None)
        when(self._file).truncate(0).thenReturn(None)

        when(builtins).open(...).thenCallOriginalImplementation()
        when(builtins).open('test.yaml', encoding='UTF-8').thenReturn(self._file)
        when(builtins).open(file='test.yaml', **kwargs).thenReturn(self._file)

        when(yaml).safe_dump({'yaml_data': 1}, ANY).thenReturn(None)

        self._subject = YamlFileConfigurationSaver()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, YamlFileConfigurationSaver)

    def test_supports(self):
        """ it returns whether it supports a destination or not """
        with patch.object(os.path, 'isfile', return_value=True):
            assert self._subject.supports({}, '/path/to/file.yaml')
            assert self._subject.supports({}, 'file.yaml')
            assert not self._subject.supports({}, '/path/to/file.json')
            assert not self._subject.supports({}, '.yaml')

        with open('test.yaml', encoding='UTF-8') as file:
            assert self._subject.supports({}, file)

    def test_supports2(self):
        """ it returns it does not support an file that does not exist """
        with patch.object(os.path, 'isfile', return_value=False):
            assert not self._subject.supports({}, '/path/to/file.yaml')
            assert not self._subject.supports({}, 'file.yaml')

    def test_save_to(self):
        """ it can save configuration to a valid file destination """
        self._subject.save_to({'yaml_data': 1}, self._file)

        verify(self._file, times=1).truncate(0)
        verify(yaml, times=1).safe_dump({'yaml_data': 1}, self._file)

    def test_save_to2(self):
        """ it can save configuration to a valid path destination """
        self._subject.save_to({'yaml_data': 1}, 'test.yaml')

        verify(self._file, times=1).truncate(0)
        verify(yaml, times=1).safe_dump({'yaml_data': 1}, self._file)
