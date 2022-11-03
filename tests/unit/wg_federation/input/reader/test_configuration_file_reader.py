from mockito import mock, when, ANY

from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader
from wg_federation.input.reader.configuration_file_reader import ConfigurationFileReader


class TestConfigurationFileReader:
    """ Test ConfigurationFileReader class """

    _configuration_loader: ConfigurationLoader = mock()
    _logger = mock()

    _subject: ConfigurationFileReader = None

    def setup(self):
        """ Constructor """
        when(self._configuration_loader).load_all_if_exists(ANY(tuple)).thenReturn({'valid': 1})

        self._subject = ConfigurationFileReader(
            logger=self._logger,
            configuration_loader=self._configuration_loader,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ConfigurationFileReader)

    def test_load_all(self):
        """ it loads all the configuration files in order """
        assert {'valid': 1} == self._subject.load_all()

    def test_get_sources(self):
        """ it returns current context configuration sources """
        assert isinstance(self._subject.get_sources(), tuple)
        assert len(self._subject.get_sources()) > 0
