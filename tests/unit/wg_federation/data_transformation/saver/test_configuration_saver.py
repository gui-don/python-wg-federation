from logging import Logger

import pytest
from mockito import unstub, mock, when, ANY, verify, verifyNoMoreInteractions

from wg_federation.data_transformation.saver.configuration_saver import ConfigurationSaver
from wg_federation.data_transformation.saver.configuration_saver_interface import ConfigurationSaverInterface
from wg_federation.data_transformation.saver.file.json_file_configuration_saver import JsonFileConfigurationSaver
from wg_federation.data_transformation.saver.file.yaml_file_configuration_saver import YamlFileConfigurationSaver
from wg_federation.exception.developer.data_transformation.destination_unsupported_error import \
    DestinationUnsupportedError


class TestConfigurationSaver:
    """ Test ConfigurationSaver class """

    _logger: Logger = None
    _configuration_saver_yaml: ConfigurationSaverInterface = None
    _configuration_saver_json: ConfigurationSaverInterface = None

    _subject: ConfigurationSaver = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._logger = mock()

        self._configuration_saver_yaml = mock(YamlFileConfigurationSaver)
        when(self._configuration_saver_yaml).supports(...).thenReturn(False)
        when(self._configuration_saver_yaml).supports(ANY, 'yaml').thenReturn(True)
        when(self._configuration_saver_yaml).save_to(...)
        when(self._configuration_saver_yaml).is_initialized(...).thenReturn(True)

        self._configuration_saver_json = mock(JsonFileConfigurationSaver)
        when(self._configuration_saver_json).supports(...).thenReturn(False)
        when(self._configuration_saver_json).supports(ANY, 'json').thenReturn(True)
        when(self._configuration_saver_json).save_to(...)
        when(self._configuration_saver_json).is_initialized(...).thenReturn(False)
        when(self._configuration_saver_json).initialize(...)

        self._subject = ConfigurationSaver(
            configuration_savers=(
                self._configuration_saver_yaml,
                self._configuration_saver_json,
            ),
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ConfigurationSaver)

    def test_save(self):
        """ it can save a configuration without an explicit ConfigurationSaver """
        self._subject.save({'data': 1}, 'yaml')
        self._subject.save_try({'try': 1}, 'yaml')

        verify(self._configuration_saver_yaml, times=1).save_to({'data': 1}, 'yaml')
        verify(self._configuration_saver_yaml, times=1).save_to({'try': 1}, 'yaml')
        verifyNoMoreInteractions()

        self._subject.save({'data': 2}, 'json')
        self._subject.save_try({'try': 2}, 'json')

        verify(self._configuration_saver_json, times=1).save_to({'data': 2}, 'json')
        verify(self._configuration_saver_json, times=1).save_to({'try': 2}, 'json')
        verifyNoMoreInteractions()

    def test_save2(self):
        """ it can save a configuration with a forced ConfigurationSaver """
        self._subject.save({'data': 1}, 'yaml', JsonFileConfigurationSaver)
        self._subject.save_try({'data': 1}, 'yaml', JsonFileConfigurationSaver)

        verify(self._configuration_saver_yaml, times=0).save_to(...)
        verify(self._configuration_saver_json, times=2).save_to({'data': 1}, 'yaml')

    def test_save3(self):
        """ it raises an error when the forced ConfigurationSaver does not exist or was not registered """
        with pytest.raises(TypeError) as error:
            self._subject.save({'data': 1}, 'yaml', Logger)

        assert 'Unable to fetch ConfigurationSaver' in str(error)

    def test_save4(self):
        """ it raises an error when the destination is not supported by any ConfigurationSaver """
        with pytest.raises(DestinationUnsupportedError) as error:
            self._subject.save({'data': 1}, 'unknown')

        assert 'It seems no ConfigurationSaver supports this type of data' in str(error)

    def test_save5(self):
        """ it can save a configuration without an explicit ConfigurationSaver """
        self._subject.save({'data': 2}, 'json')
        self._subject.save_try({'try': 2}, 'json')

        verify(self._configuration_saver_json, times=1).save_to({'data': 2}, 'json')
        verify(self._configuration_saver_json, times=1).save_to({'try': 2}, 'json')
        verify(self._configuration_saver_json, times=1).initialize({'data': 2}, 'json')
        verify(self._configuration_saver_json, times=1).initialize({'try': 2}, 'json')
        verifyNoMoreInteractions()

    def test_save_try2(self):
        """ it does not raise any error even if the destination is not supported by any ConfigurationSaver """
        self._subject.save_try({'data': 1}, 'unknown')

        verify(self._configuration_saver_yaml, times=0).save_to(...)
        verify(self._configuration_saver_json, times=0).save_to(...)
