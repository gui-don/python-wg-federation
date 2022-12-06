import pytest
from mockito import unstub, mock, when, verify
from pydantic import SecretStr

from wg_federation.crypto.data.encrypted_message import EncryptedMessage
from wg_federation.crypto.message_encrypter import MessageEncrypter
from wg_federation.data_transformation.saver.can_save_configuration_interface import CanSaveConfigurationInterface
from wg_federation.data_transformation.saver.configuration_saver import ConfigurationSaver
from wg_federation.data_transformation.saver.proxy.encrypt_configuration_saver_proxy import \
    EncryptConfigurationSaverProxy


class TestEncryptConfigurationSaverProxy:
    """ Test EncryptConfigurationSaverProxy class """

    _encrypted_message: EncryptedMessage = None

    _message_encrypter: MessageEncrypter = None
    _configuration_saver: CanSaveConfigurationInterface = None

    _subject: EncryptConfigurationSaverProxy = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._encrypted_message = mock()
        when(self._encrypted_message).hex_dict().thenReturn({'encrypted': True})

        self._message_encrypter = mock()
        when(self._message_encrypter).encrypt(...).thenReturn(self._encrypted_message)

        self._configuration_saver = mock(ConfigurationSaver)
        when(self._configuration_saver).save(...)
        when(self._configuration_saver).save_try(...)

        self._subject = EncryptConfigurationSaverProxy(
            configuration_saver=self._configuration_saver,
            message_encrypter=self._message_encrypter
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, EncryptConfigurationSaverProxy)

    def test_save(self):
        """ it encrypts all secrets of a configuration before saving it """
        self._subject.save({'data': 1, 'secret': SecretStr('test')}, 'yaml')

        verify(self._message_encrypter, times=1).encrypt(b'test')
        verify(self._configuration_saver, times=1).save({'data': 1, 'secret': {'encrypted': True}}, 'yaml', None)

    def test_save_try(self):
        """ it encrypts all secrets of a configuration before saving it """
        self._subject.save_try({'try': {'test': SecretStr('value')}}, 'yaml')
        self._subject.save_try({'try': 'notsecret'}, 'yaml', SecretStr)

        verify(self._message_encrypter, times=1).encrypt(b'value')
        verify(self._configuration_saver, times=1).save_try({'try': {'test': {'encrypted': True}}}, 'yaml', None)
        verify(self._configuration_saver, times=1).save_try({'try': 'notsecret'}, 'yaml', SecretStr)
