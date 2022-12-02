import base64
from types import ModuleType

import pytest
from mockito import mock, unstub, when, ANY
from nacl.public import PrivateKey

from wg_federation.crypto.wireguard_key_generator import WireguardKeyGenerator


class TestWireguardKeyGenerator:
    """ Test WireguardKeyGenerator class """

    _nacl_key_pair: ModuleType = None
    _nacl_private_key: ModuleType = None

    _nacl_public_lib: ModuleType = None
    _cryptodome_random_lib: ModuleType = None

    _subject: WireguardKeyGenerator = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    # pylint: disable=unnecessary-dunder-call
    def setup_method(self):
        """ Constructor """
        self._nacl_key_pair = mock({'public_key': b'public_key'}, spec=PrivateKey)
        when(self._nacl_key_pair).__bytes__().thenReturn(b'private_key')

        self._nacl_private_key = mock(PrivateKey)
        when(self._nacl_private_key).__bytes__().thenReturn(b'private_key')

        static_private_key = mock(PrivateKey)
        when(static_private_key).generate().thenReturn(self._nacl_private_key)
        when(static_private_key).__call__(...).thenReturn(self._nacl_key_pair)

        self._nacl_public_lib: ModuleType = mock({'PrivateKey': static_private_key})

        self._cryptodome_random_lib = mock()
        when(self._cryptodome_random_lib).get_random_bytes(ANY).thenReturn(b'random')

        self._subject = WireguardKeyGenerator(
            nacl_public_lib=self._nacl_public_lib,
            cryptodome_random_lib=self._cryptodome_random_lib,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, WireguardKeyGenerator)

    def test_generate_key_pairs(self):
        """ it generates wireguard private/public key pairs """
        assert (
            base64.b64encode(b'private_key').decode('ascii'),
            base64.b64encode(b'public_key').decode('ascii'),
        ) == self._subject.generate_key_pairs()

    def test_generate_psk(self):
        """ it generates a wireguard pre-shared key """
        assert base64.b64encode(b'random').decode('ascii') == self._subject.generate_psk()
