import argparse
import builtins

import Cryptodome
import pytest
import xdg
from mockito import mock, when, kwargs, unstub
from pydantic import SecretStr

from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver
from wg_federation.data.input.user_input import UserInput
from wg_federation.exception.developer.crypto.root_passphrase_not_set import RootPassphraseNotSet
from wg_federation.exception.developer.crypto.salt_file_not_found import SaltFileNotFound


class TestCryptographicKeyDeriver:
    """ Test CryptographicKeyDeriver class """

    _user_input: UserInput = None
    _subject: CryptographicKeyDeriver = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup()

    def setup(self):
        """ Constructor """
        argument_parser = mock({'prog': 'program'})
        when(xdg).xdg_data_home().thenReturn('/home/data_path')
        when(argparse).ArgumentParser().thenReturn(argument_parser)

        root_passphrase = mock(SecretStr)
        when(root_passphrase).get_secret_value().thenReturn('very secret')
        self._user_input = mock({'root_passphrase': root_passphrase})

        file = mock()
        when(file).read().thenReturn('salt')
        # Yes: necessary because it’s a stub
        # pylint: disable=unnecessary-dunder-call
        when(file).__enter__(...).thenReturn(file)
        when(file).__exit__(...).thenReturn('salt')

        when(builtins).open('/home/data_path/program/passphrase.salt', ...).thenReturn(file)

        self._subject = CryptographicKeyDeriver(
            user_input=self._user_input,
        )

    def teardown(self):
        """ Resets mocks """
        unstub()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, CryptographicKeyDeriver)

    def test_get_salt_full_path(self):
        """ it returns the path of the salt file """
        assert '/home/data_path/program/passphrase.salt' == self._subject.get_salt_full_path()

    def test_get_cache_status(self):
        """ it returns its cache status """
        assert self._subject.get_cache_status()

    def test_derive_32b_key_from_root_passphrase(self):
        """ it raises an error if the user input have no passphrase set """
        _user_input = mock({'root_passphrase': None})
        _subject = CryptographicKeyDeriver(
            user_input=_user_input,
        )

        with pytest.raises(RootPassphraseNotSet) as error:
            _subject.derive_32b_key_from_root_passphrase()

        assert 'The root passphrase was not set' in str(error)

    def test_derive_32b_key_from_root_passphrase2(self):
        """ it raises an error if the salt file cannot be found """
        when(builtins).open('/home/data_path/program/passphrase.salt', ...).thenRaise(FileNotFoundError())

        with pytest.raises(SaltFileNotFound) as error:
            self._subject.derive_32b_key_from_root_passphrase()

        assert 'Salt file /home/data_path/program/passphrase.salt cannot be found' in str(error)

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
