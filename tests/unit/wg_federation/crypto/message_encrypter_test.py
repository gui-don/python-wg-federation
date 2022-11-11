from Cryptodome.Cipher import AES
from mockito import mock, unstub, when, kwargs

from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver
from wg_federation.crypto.message_encrypter import MessageEncrypter


class TestMessageEncrypter:
    """ Test MessageEncrypter class """

    _cryptographic_key_deriver: CryptographicKeyDeriver = mock()
    _cryptodome_aes: AES = mock()
    _subject: MessageEncrypter = None

    def setup_method(self):
        """ Constructor """

        when(self._cryptographic_key_deriver).derive_32b_key_from_root_passphrase().thenReturn(b'key')

        cipher = mock({'nonce': b'nonce'})
        when(cipher).encrypt_and_digest(...).thenReturn((b'ciphertext', b'digest',))
        when(cipher).decrypt_and_verify(b'ciphertext', b'digest').thenReturn(b'message')

        when(self._cryptodome_aes).new(key=b'key', **kwargs).thenReturn(cipher)

        self._subject = MessageEncrypter(
            cryptographic_key_deriver=self._cryptographic_key_deriver,
            cryptodome_aes=self._cryptodome_aes,
        )

    def teardown_method(self):
        """ Resets mocks """
        unstub()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, MessageEncrypter)

    def test_encrypt(self):
        """ it encrypts a given message """
        result = self._subject.encrypt(b'message')

        assert result.get('ciphertext') == b'ciphertext'.hex()
        assert result.get('digest') == b'digest'.hex()
        assert result.get('nonce') == b'nonce'.hex()

    def test_decrypt(self):
        """ it decrypts a given message """
        assert b'message' == self._subject.decrypt(b'ciphertext'.hex(), b'nonce'.hex(), b'digest'.hex())
