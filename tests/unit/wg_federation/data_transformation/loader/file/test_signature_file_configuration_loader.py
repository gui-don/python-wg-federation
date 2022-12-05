import builtins
from io import TextIOWrapper

import pytest
from mockito import mock, unstub, when, kwargs, ANY, verify

from wg_federation.data_transformation.loader.file.signature_file_configuration_reader import \
    SignatureFileConfigurationLoader


# pylint: disable=duplicate-code

class TestSignatureFileConfigurationLoader:
    """ Test SignatureFileConfigurationLoader class """

    _file = None
    _exist_path = None
    _non_exist_path = None

    _os_path_lib = None
    _subject: SignatureFileConfigurationLoader = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._file = mock({'name': 'test.sig'}, spec=TextIOWrapper)
        # pylint: disable=unnecessary-dunder-call
        when(self._file).__enter__().thenReturn(self._file)
        when(self._file).__exit__(...).thenReturn(None)
        when(self._file).seek(ANY).thenReturn(None)
        when(self._file).read().thenReturn('signature')

        self._os_path_lib = mock()
        when(self._os_path_lib).exists(...).thenReturn(True)
        when(self._os_path_lib).exists('unknown.signature').thenReturn(False)

        when(builtins).open(...).thenCallOriginalImplementation()
        when(builtins).open(file='source.signature', **kwargs).thenReturn(self._file)

        self._subject = SignatureFileConfigurationLoader(os_path_lib=self._os_path_lib)

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, SignatureFileConfigurationLoader)

    def test_supports(self):
        """ it returns whether it supports a source or not """
        assert True is self._subject.supports('/path/to/file.digest')
        assert True is self._subject.supports('file.sha256')
        assert True is self._subject.supports('/test.md5')
        assert True is self._subject.supports('/path/to/file.sig')
        assert False is self._subject.supports('/path/to/file.SIGNATURE')
        assert False is self._subject.supports('.digest')

    def test_supports2(self):
        """ it returns it does not support an file that does not exist """
        assert False is self._subject.supports('unknown.signature')

    def test_load_from(self):
        """ it can load configuration from a valid source """
        assert {'test.sig': 'signature'} == self._subject.load_from('source.signature')
        verify(self._file, times=1).seek(0)

    def test_load_from2(self):
        """ it can load configuration from a valid opened file handler """
        assert {'test.sig': 'signature'} == self._subject.load_from(self._file)
        verify(self._file, times=1).seek(0)
