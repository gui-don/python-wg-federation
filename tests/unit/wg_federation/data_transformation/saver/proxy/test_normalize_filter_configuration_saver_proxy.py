from ipaddress import IPv4Interface

import pytest
from mockito import unstub, when, mock, verify

from wg_federation.data.state.interface_status import InterfaceStatus
from wg_federation.data_transformation.saver.can_save_configuration_interface import CanSaveConfigurationInterface
from wg_federation.data_transformation.saver.proxy.normalize_filter_configuration_saver_proxy import \
    NormalizeFilterConfigurationSaverProxy
from wg_federation.data_transformation.saver.proxy.sign_configuration_saver_proxy import SignConfigurationSaverProxy


class TestNormalizeFilterConfigurationSaverProxy:
    """ Test NormalizeFilterConfigurationSaverProxy class """

    _configuration_saver: CanSaveConfigurationInterface = None

    _subject: NormalizeFilterConfigurationSaverProxy = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._configuration_saver = mock()
        when(self._configuration_saver).save(...)

        self._subject = NormalizeFilterConfigurationSaverProxy(
            configuration_saver=self._configuration_saver,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, NormalizeFilterConfigurationSaverProxy)

    def test_save(self):
        """ it converts immutable types to mutable """

        self._subject.save({'data': ('content', {'empty': (), 'one': 1}), 'str': 'string'}, 'destination_path')
        self._subject.save_try(
            {'data': {'content_try', }, 'ip': IPv4Interface('192.168.1.0/24'), 'enum': InterfaceStatus.ACTIVE},
            'destination_path2',
            SignConfigurationSaverProxy
        )

        verify(self._configuration_saver, times=1).save(
            {'data': ['content', {'one': 1}], 'str': 'string'},
            'destination_path',
            None
        )

        verify(self._configuration_saver, times=1).save_try(
            {'data': ['content_try'], 'ip': '192.168.1.0/24', 'enum': 'ACTIVE'},
            'destination_path2',
            SignConfigurationSaverProxy
        )
