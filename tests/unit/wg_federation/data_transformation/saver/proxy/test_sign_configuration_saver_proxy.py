import pytest
from mockito import unstub, when, verify, mock

from wg_federation.crypto.message_signer import MessageSigner
from wg_federation.data_transformation.configuration_location_finder import ConfigurationLocationFinder
from wg_federation.data_transformation.saver.can_save_configuration_interface import CanSaveConfigurationInterface
from wg_federation.data_transformation.saver.proxy.sign_configuration_saver_proxy import SignConfigurationSaverProxy


class TestSignConfigurationSaverProxy:
    """ Test SignConfigurationSaverProxy class """

    _configuration_location_finder: ConfigurationLocationFinder = None
    _configuration_saver: CanSaveConfigurationInterface = None
    _message_signer: MessageSigner = None
    _digest_configuration_saver: CanSaveConfigurationInterface = None

    _subject: SignConfigurationSaverProxy = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._message_signer = mock()
        when(self._message_signer).sign(str({'data': 'content'})).thenReturn(('mac', 'nonce',))
        when(self._message_signer).sign(str({'data': 'content_try'})).thenReturn(('mactry', 'noncetry',))

        self._configuration_location_finder = mock()
        when(self._configuration_location_finder).state_digest_belongs_to_state().thenReturn(True)
        when(self._configuration_location_finder).state_digest().thenReturn('digest_location')

        self._digest_configuration_saver = mock()
        when(self._digest_configuration_saver).save({'digest': 'mac'}, 'digest_location')

        self._configuration_saver = mock()
        when(self._configuration_saver).save(...)

        self._subject = SignConfigurationSaverProxy(
            configuration_location_finder=self._configuration_location_finder,
            configuration_saver=self._configuration_saver,
            message_signer=self._message_signer,
            digest_configuration_saver=self._digest_configuration_saver,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, SignConfigurationSaverProxy)

    def test_save(self):
        """ it signs content before saving it """

        self._subject.save({'data': 'content'}, 'destination_path')
        self._subject.save_try({'data': 'content_try'}, 'destination_path2', SignConfigurationSaverProxy)

        verify(self._configuration_saver, times=1).save(
            {'data': {'data': 'content'}, 'nonce': 'nonce', 'digest': 'mac'},
            'destination_path',
            None
        )

        verify(self._configuration_saver, times=1).save_try(
            {'data': {'data': 'content_try'}, 'nonce': 'noncetry', 'digest': 'mactry'},
            'destination_path2',
            SignConfigurationSaverProxy
        )

    def test_save2(self):
        """ it signs content before saving it with a side digest file """

        when(self._configuration_location_finder).state_digest_belongs_to_state().thenReturn(False)
        self._subject.save({'data': 'content'}, 'destination_path')
        self._subject.save_try({'data': 'content_try'}, 'destination_path2', SignConfigurationSaverProxy)

        verify(self._digest_configuration_saver, times=1).save({'digest': 'mac'}, 'digest_location')
        verify(self._digest_configuration_saver, times=1).save({'digest': 'mactry'}, 'digest_location')

        verify(self._configuration_saver, times=1).save(
            {'data': {'data': 'content'}, 'nonce': 'nonce'},
            'destination_path',
            None
        )
        verify(self._configuration_saver, times=1).save_try(
            {'data': {'data': 'content_try'}, 'nonce': 'noncetry'},
            'destination_path2',
            SignConfigurationSaverProxy
        )
