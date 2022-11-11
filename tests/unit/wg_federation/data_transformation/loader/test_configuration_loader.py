import pytest
from mockito import when, ANY, mock, verify, forget_invocations

from wg_federation.data_transformation.loader.can_load_configuration_interface import CanLoadConfigurationInterface
from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader
from wg_federation.exception.developer.data_transformation.source_unsupported_error import SourceUnsupportedError


class TestConfigurationLoader:
    """ Test ConfigurationLoader class """

    _working_configuration_loader = mock()
    _working_configuration_loader2 = mock()
    _silent_configuration_loader = mock()
    _logger = mock()

    _subject: ConfigurationLoader = None

    def setup_method(self):
        """ Constructor """

        when(self._working_configuration_loader).supports(ANY(str)).thenReturn(False)
        when(self._working_configuration_loader).supports('source1').thenReturn(True)
        when(self._working_configuration_loader).get_supported_source().thenReturn('valid')
        when(self._working_configuration_loader).load_from(ANY(str)).thenReturn(
            {'override': 1, 'list': [1], 'single': 1, 'dict': {'one': 1}}
        )

        when(self._working_configuration_loader2).supports(ANY(str)).thenReturn(False)
        when(self._working_configuration_loader2).supports('source2').thenReturn(True)
        when(self._working_configuration_loader2).get_supported_source().thenReturn('valid2')
        when(self._working_configuration_loader2).load_from(ANY(str)).thenReturn(
            {'override': 2, 'list': [2], 'dict': {'two': 2}}
        )

        when(self._silent_configuration_loader).get_supported_source().thenReturn('unknown')
        when(self._silent_configuration_loader).supports(ANY(str)).thenReturn(False)

        self._subject = ConfigurationLoader(
            configuration_loaders=(
                self._silent_configuration_loader,
                self._working_configuration_loader,
                self._working_configuration_loader2,
            ),
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ConfigurationLoader)
        assert isinstance(self._subject, CanLoadConfigurationInterface)

    def test_load(self):
        """ it can load a configuration from a valid source """
        result = self._subject.load('any', 'valid')

        verify(self._working_configuration_loader, times=1).load_from('any')
        verify(self._working_configuration_loader2, times=0).load_from(ANY)
        verify(self._silent_configuration_loader, times=0).load_from(ANY)
        assert {'override': 1, 'list': [1], 'single': 1, 'dict': {'one': 1}} == result

        forget_invocations(self._working_configuration_loader)

        result = self._subject.load('any2', 'valid2')

        verify(self._working_configuration_loader, times=0).load_from(ANY)
        verify(self._working_configuration_loader2, times=1).load_from('any2')
        verify(self._silent_configuration_loader, times=0).load_from(ANY)

        assert {'override': 2, 'list': [2], 'dict': {'two': 2}} == result

    def test_load2(self):
        """ it can load a configuration from a valid source, automatically """
        result = self._subject.load('source2')

        verify(self._working_configuration_loader, times=0).load_from(ANY)
        verify(self._working_configuration_loader2, times=1).load_from('source2')
        verify(self._silent_configuration_loader, times=0).load_from(ANY)

        assert {'override': 2, 'list': [2], 'dict': {'two': 2}} == result

    def test_load3(self):
        """ it raises an error if no configuration loader is found for the given source """
        with pytest.raises(SourceUnsupportedError) as error:
            self._subject.load('unknown')

        assert 'Could not load any configuration' in str(error)

    def test_load_if_exists(self):
        """ it returns None when the source cannot be processed """
        assert isinstance(self._subject.load_if_exists('unknown'), dict)
        assert not self._subject.load_if_exists('unknown')

    def test_load_all(self):
        """ it can load from multiple sources and unify them into a single configuration """

        result = self._subject.load_all(('source1', 'source2'))

        assert {'override': 2, 'list': [1, 2], 'single': 1, 'dict': {'one': 1, 'two': 2}} == result

    def test_load_all2(self):
        """ it raises an error when loading from multiple sources and one of them cannot be processed """
        with pytest.raises(SourceUnsupportedError) as error:
            self._subject.load_all(('source1', 'unknown', 'source2'))

        assert 'Could not load any configuration' in str(error)

    def test_load_all_if_exists(self):
        """ it can load from multiple sources, even when some cannot be processed, into a single configuration """

        result = self._subject.load_all_if_exists(('source1', 'unknown', 'source2'))

        assert {'override': 2, 'list': [1, 2], 'single': 1, 'dict': {'one': 1, 'two': 2}} == result
