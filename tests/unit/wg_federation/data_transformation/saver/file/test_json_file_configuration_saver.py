import builtins
import json
from io import TextIOWrapper

import pytest
from mockito import mock, unstub, when, kwargs, ANY, verify

from wg_federation.data_transformation.saver.file.json_file_configuration_saver import JsonFileConfigurationSaver


# pylint: disable=duplicate-code


class TestJsonFileConfigurationSaver:
    """ Test JsonFileConfigurationSaver class """

    _file = None
    _non_exist_parent_path = None

    _pathlib_lib = None
    _subject: JsonFileConfigurationSaver = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._file = mock(spec=TextIOWrapper)
        # pylint: disable=unnecessary-dunder-call
        when(self._file).__enter__().thenReturn(self._file)
        when(self._file).__exit__(...).thenReturn(None)
        when(self._file).truncate(ANY).thenReturn(None)
        when(self._file).write(ANY).thenReturn(None)

        _exist_path = mock()
        when(_exist_path).exists().thenReturn(True)

        self._non_exist_parent_path = mock()
        when(self._non_exist_parent_path).mkdir(...)

        _non_exist_path = mock({'parents': [self._non_exist_parent_path]})
        when(_non_exist_path).exists().thenReturn(False)

        self._pathlib_lib = mock()
        when(self._pathlib_lib).Path(...).thenReturn(_exist_path)
        when(self._pathlib_lib).Path('unknown.json').thenReturn(_non_exist_path)

        when(builtins).open(...).thenCallOriginalImplementation()
        when(builtins).open(file='destination.json', **kwargs).thenReturn(self._file)

        when(json).dump(...).thenCallOriginalImplementation()
        when(json).dump({'data': 'json'}, self._file)

        self._subject = JsonFileConfigurationSaver(pathlib_lib=self._pathlib_lib)

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, JsonFileConfigurationSaver)

    def test_supports(self):
        """ it returns whether it supports a source or not """
        assert True is self._subject.supports({}, '/path/to/file.json')
        assert True is self._subject.supports({}, 'file.json')
        assert True is self._subject.supports({}, '/path/to/file.JSON')
        assert False is self._subject.supports({}, '/path/to/file.yml')
        assert False is self._subject.supports({}, '.json')

    def test_supports2(self):
        """ it returns it does not support types that are not strings or file handlers """
        assert False is self._subject.supports({}, b'invalid_bytes')

    def test_save_to(self):
        """ it can save configuration to a valid file destination """
        self._subject.save_to({'json_data': 1}, self._file)

        verify(self._file, times=1).truncate(0)
        verify(json, times=1).dump({'json_data': 1}, self._file)
        verify(json, times=1).dump({'json_data': 1}, self._file)

    def test_save_to2(self):
        """ it can save configuration to a valid path destination """
        self._subject.save_to({'json_data': 1}, 'destination.json')

        verify(self._file, times=1).truncate(0)
        verify(json, times=1).dump({'json_data': 1}, self._file)

    def test_is_initialized(self):
        """ it returns whether the destination/data is initialized """
        assert self._subject.is_initialized({}, 'destination.json')

    def test_is_initialized2(self):
        """ it returns when it is not initialized because the file does not exist """
        assert not self._subject.is_initialized({}, 'unknown.json')

    def test_initialize(self):
        """ it initializes """
        self._subject.initialize({}, 'unknown.json')

        verify(self._non_exist_parent_path, times=1).mkdir(...)
