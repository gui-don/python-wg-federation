import builtins
from io import TextIOWrapper

import pytest
import yaml
from mockito import mock, unstub, when, kwargs, ANY, verify

from wg_federation.data_transformation.loader.file.yaml_file_configuration_loader import YamlFileConfigurationLoader

# pylint: disable=duplicate-code


class TestYamlFileConfigurationLoader:
    """ Test YamlFileConfigurationLoader class """

    _file = None
    _exist_path = None
    _non_exist_path = None

    _pathlib_lib = None
    _subject: YamlFileConfigurationLoader = None

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
        when(self._file).seek(ANY).thenReturn(None)

        self._exist_path = mock()
        when(self._exist_path).exists().thenReturn(True)

        self._non_exist_path = mock()
        when(self._non_exist_path).exists().thenReturn(False)

        self._pathlib_lib = mock()
        when(self._pathlib_lib).Path(...).thenReturn(self._exist_path)
        when(self._pathlib_lib).Path('unknown.yaml').thenReturn(self._non_exist_path)

        when(builtins).open(...).thenCallOriginalImplementation()
        when(builtins).open(file='source.yaml', **kwargs).thenReturn(self._file)

        when(yaml).safe_load(...).thenCallOriginalImplementation()
        when(yaml).safe_load(self._file).thenReturn({'yaml_data': 1})

        self._subject = YamlFileConfigurationLoader(pathlib_lib=self._pathlib_lib)

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, YamlFileConfigurationLoader)

    def test_supports(self):
        """ it returns whether it supports a source or not """
        assert True is self._subject.supports('/path/to/file.yaml')
        assert True is self._subject.supports('file.yaml')
        assert True is self._subject.supports('/path/to/file.yml')
        assert True is self._subject.supports('/path/to/file.YAML')
        assert False is self._subject.supports('.yaml')

    def test_supports2(self):
        """ it returns it does not support an file that does not exist """
        assert False is self._subject.supports('unknown.yaml')

    def test_load_from(self):
        """ it can load configuration from a valid source """
        assert {'yaml_data': 1} == self._subject.load_from('source.yaml')
        verify(self._file, times=1).seek(0)

    def test_load_from2(self):
        """ it can load configuration from a valid source, and makes sure to always a dict """
        when(yaml).safe_load(self._file).thenReturn('')

        assert {} == self._subject.load_from('source.yaml')
        verify(self._file, times=1).seek(0)

    def test_load_from3(self):
        """ it can load configuration from a valid opened file handler """
        assert {'yaml_data': 1} == self._subject.load_from(self._file)
        verify(self._file, times=1).seek(0)
