from random import Random

import Cryptodome
import pytest
from mockito import mock, when, kwargs, unstub, verify
from pydantic import SecretStr

from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver
from wg_federation.data.input.user_input import UserInput
from wg_federation.data_transformation.configuration_location_finder import ConfigurationLocationFinder
from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader
from wg_federation.data_transformation.saver.configuration_saver import ConfigurationSaver
from wg_federation.exception.developer.crypto.root_passphrase_not_set import RootPassphraseNotSet


class TestCryptographicKeyDeriver:
    """ Test CryptographicKeyDeriver class """

    # pylint: disable=duplicate-code
    _user_input: UserInput = None
    _configuration_location_finder: ConfigurationLocationFinder = None
    _configuration_loader: ConfigurationLoader = None
    _configuration_saver: ConfigurationSaver = None
    _cryptodome_random_lib: Random = None

    _subject: CryptographicKeyDeriver = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """
        secret = mock(SecretStr)
        when(secret).get_secret_value().thenReturn('very secret')

        self._user_input = mock({'root_passphrase': secret})

        self._configuration_location_finder = mock()
        when(self._configuration_location_finder).salt().thenReturn('salt_location')

        self._configuration_loader: ConfigurationLoader = mock()
        when(self._configuration_loader).load('salt_location').thenReturn({'where': 'salt'})

        self._configuration_saver: ConfigurationSaver = mock()
        self._cryptodome_random_lib: Random = mock()
        when(self._cryptodome_random_lib).get_random_bytes(32).thenReturn(b'random')

        root_passphrase = mock(SecretStr)
        when(root_passphrase).get_secret_value().thenReturn('very secret')
        self._user_input = mock({'root_passphrase': root_passphrase})

        self._subject = CryptographicKeyDeriver(
            user_input=self._user_input,
            configuration_location_finder=self._configuration_location_finder,
            configuration_loader=self._configuration_loader,
            configuration_saver=self._configuration_saver,
            cryptodome_random_lib=self._cryptodome_random_lib,
        )

    def teardown_method(self):
        """ Resets mocks """
        unstub()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, CryptographicKeyDeriver)

    def test_get_cache_status(self):
        """ it returns its cache status """
        assert self._subject.get_cache_status()

    def test_create_salt(self):
        """ it creates a new salt """
        self._subject.create_salt()
        verify(self._configuration_saver, times=1).save({'raw': b'random'}, 'salt_location')

    def test_derive_32b_key_from_root_passphrase(self):
        """ it raises an error if the user input have no passphrase set """
        _user_input = mock({'root_passphrase': None})
        _subject = CryptographicKeyDeriver(
            user_input=_user_input,
            configuration_location_finder=self._configuration_location_finder,
            configuration_loader=self._configuration_loader,
            configuration_saver=self._configuration_saver,
            cryptodome_random_lib=self._cryptodome_random_lib,
        )

        with pytest.raises(RootPassphraseNotSet) as error:
            _subject.derive_32b_key_from_root_passphrase()

        assert 'The root passphrase was not set' in str(error)

    def test_derive_32b_key_from_root_passphrase3(self):
        """ it gets a 32 bits key derived from a root passphrase """
        when(Cryptodome.Protocol.KDF).PBKDF2(
            password='very secret',
            salt='salt'.encode('UTF-8'),
            dkLen=32,
            count=1111,
            **kwargs
        ).thenReturn(b'result1')

        assert b'result1' == self._subject.derive_32b_key_from_root_passphrase()

    def test_clear_cache(self):
        """ it clears its cache """
        self._subject.clear_cache()
