import builtins
import json
import os
from io import TextIOWrapper
from unittest.mock import patch

import pytest
from mockito import when, mock, unstub, ANY, verify, kwargs

from wg_federation.data_transformation.saver.file.json_file_configuration_saver import JsonFileConfigurationSaver


# pylint: disable=duplicate-code


class TestJsonFileConfigurationSaver:
    """ Test JsonFileConfigurationSaver class """

    _file = None
    _subject: JsonFileConfigurationSaver = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._file = mock({'name': 'test.json'}, spec=TextIOWrapper)
        # pylint: disable=unnecessary-dunder-call
        when(self._file).__enter__(...).thenReturn(self._file)
        when(self._file).__exit__(...).thenReturn(None)
        when(self._file).truncate(0).thenReturn(None)

        when(builtins).open(...).thenCallOriginalImplementation()
        when(builtins).open('test.json', encoding='UTF-8').thenReturn(self._file)
        when(builtins).open(file='test.json', **kwargs).thenReturn(self._file)

        when(json).dump({'json_data': 1}, ANY).thenReturn(None)

        self._subject = JsonFileConfigurationSaver()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, JsonFileConfigurationSaver)

    def test_supports(self):
        """ it returns whether it supports a destination or not """
        with patch.object(os.path, 'isfile', return_value=True):
            assert self._subject.supports({}, '/path/to/file.json')
            assert self._subject.supports({}, 'file.json')
            assert not self._subject.supports({}, '/path/to/file.yml')
            assert not self._subject.supports({}, '.json')

        with open('test.json', encoding='UTF-8') as file:
            assert self._subject.supports({}, file)

    def test_supports2(self):
        """ it returns it does not support an file that does not exist """
        with patch.object(os.path, 'isfile', return_value=False):
            assert not self._subject.supports({}, '/path/to/file.json')
            assert not self._subject.supports({}, 'file.json')

    def test_save_to(self):
        """ it can save configuration to a valid file destination """
        self._subject.save_to({'json_data': 1}, self._file)

        verify(self._file, times=1).truncate(0)
        verify(json, times=1).dump({'json_data': 1}, self._file)

    def test_save_to2(self):
        """ it can save configuration to a valid path destination """
        self._subject.save_to({'json_data': 1}, 'test.json')

        verify(self._file, times=1).truncate(0)
        verify(json, times=1).dump({'json_data': 1}, self._file)
