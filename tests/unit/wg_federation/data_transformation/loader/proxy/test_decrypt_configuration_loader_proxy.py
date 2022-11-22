import pytest
from mockito import unstub, mock, when, verify

from wg_federation.crypto.message_encrypter import MessageEncrypter
from wg_federation.data_transformation.loader.can_load_configuration_interface import CanLoadConfigurationInterface
from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader
from wg_federation.data_transformation.loader.proxy.decrypt_configuration_loader_proxy import \
    DecryptConfigurationLoaderProxy


class TestDecryptConfigurationLoaderProxy:
    """ Test DecryptConfigurationLoaderProxy class """

    _message_encrypter: MessageEncrypter = None
    _configuration_loader: CanLoadConfigurationInterface = None

    _subject: DecryptConfigurationLoaderProxy = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._message_encrypter = mock()
        when(self._message_encrypter).decrypt(...).thenReturn(b'cleartext_secret')

        data = {'data': 1, 'secret': {'ciphertext': b'text'.hex(), 'nonce': b'nonce'.hex(), 'digest': b'digest'.hex()}}
        self._configuration_loader = mock(ConfigurationLoader)
        when(self._configuration_loader).load_if_exists(...).thenReturn(data.copy())
        when(self._configuration_loader).load(...).thenReturn(data.copy())
        when(self._configuration_loader).load_all_if_exists(...).thenReturn(data.copy())
        when(self._configuration_loader).load_all(...).thenReturn(data.copy())

        self._subject = DecryptConfigurationLoaderProxy(
            configuration_loader=self._configuration_loader,
            message_encrypter=self._message_encrypter
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, DecryptConfigurationLoaderProxy)

    def test_loadx(self):
        """ it decrypts configurations after loading them """
        assert {'data': 1, 'secret': 'cleartext_secret'} == self._subject.load('source')
        assert {'data': 1, 'secret': 'cleartext_secret'} == self._subject.load_if_exists('source')
        assert {'data': 1, 'secret': 'cleartext_secret'} == self._subject.load_all_if_exists(('source', 'source2',))
        assert {'data': 1, 'secret': 'cleartext_secret'} == self._subject.load_all(('source', 'source2',))

        verify(self._message_encrypter, times=4).decrypt(...)

    def test_loadx2(self):
        """ it does not try to decrypt anything if no encrypted message is found """
        when(self._configuration_loader).load(...).thenReturn({'data': 'unencrypted'})
        when(self._configuration_loader).load_if_exists(...).thenReturn({'data': 'unencrypted'})
        when(self._configuration_loader).load(...).thenReturn({'data': 'unencrypted'})
        when(self._configuration_loader).load_all_if_exists(...).thenReturn({'data': 'unencrypted'})
        when(self._configuration_loader).load_all(...).thenReturn({'data': 'unencrypted'})

        assert {'data': 'unencrypted'} == self._subject.load('source')
        assert {'data': 'unencrypted'} == self._subject.load_if_exists('source')
        assert {'data': 'unencrypted'} == self._subject.load_all_if_exists(('source',))
        assert {'data': 'unencrypted'} == self._subject.load_all(('source',))

        verify(self._message_encrypter, times=0).decrypt(...)

    def test_loadx3(self):
        """ it decrypts any secret, even in a sub level in the configuration tree """
        when(self._configuration_loader).load(...).thenReturn({
            'data': {'enclosed': {'ciphertext': b'text'.hex(), 'nonce': b'nonce'.hex(), 'digest': b'digest'.hex()}},
            'second': {'ciphertext': b'text'.hex(), 'nonce': b'nonce'.hex(), 'digest': b'digest'.hex()}
        })

        assert {'data': {'enclosed': 'cleartext_secret'}, 'second': 'cleartext_secret'} == self._subject.load('source')

        verify(self._message_encrypter, times=2).decrypt(...)
