from unittest.mock import MagicMock

import pytest

from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader


class TestConfigurationLoader:
    """ Test ConfigurationLoader class """

    _working_configuration_loader = MagicMock()
    _silent_configuration_loader = MagicMock()
    _logger = MagicMock()

    _subject: ConfigurationLoader = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mocks between tests """
        self._logger.reset_mock()

    def setup(self):
        """ Constructor """

        self._working_configuration_loader.get_supported_source = MagicMock(return_value='valid')
        self._working_configuration_loader.load_from_all = MagicMock(return_value={'success': 1})

        self._silent_configuration_loader.get_supported_source = MagicMock(return_value='unknowns')

        self._subject = ConfigurationLoader(
            configuration_loaders=[self._silent_configuration_loader, self._working_configuration_loader, ],
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ConfigurationLoader)

    def test_load(self):
        """ it can load configurations from valid sources """
        result = self._subject.load('valid', ('source1', 'source2', 'source3'))

        self._working_configuration_loader.load_from_all.assert_called_with(('source1', 'source2', 'source3'))
        self._silent_configuration_loader.load_from_all.assert_not_called()
        assert {'success': 1} == result

    def test_load2(self):
        """ it raises an error when no ConfigurationLoader is compatible with given source kind """

        with pytest.raises(RuntimeError) as error:
            self._subject.load('not_found', ('source1',))

        assert 'Could not load any configuration' in str(error.value)
        self._working_configuration_loader.load_from_all.assert_not_called()
        self._silent_configuration_loader.load_from_all.assert_not_called()
