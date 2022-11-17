import pytest
from Cryptodome.Cipher import AES
from Cryptodome.Hash import Poly1305
from mockito import mock, unstub, when, ANY

from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver
from wg_federation.crypto.message_signer import MessageSigner
from wg_federation.exception.user.data_transformation.state_signature_cannot_be_verified import \
    StateSignatureCannotBeVerified


class TestMessageSigner:
    """ Test MessageSigner class """

    _cryptographic_key_deriver: CryptographicKeyDeriver = mock()
    _cryptodome_poly1305: Poly1305 = mock()
    _subject: MessageSigner = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        when(self._cryptographic_key_deriver).derive_32b_key_from_root_passphrase().thenReturn(b'key')
        mac = mock({'nonce': b'nonce'})
        when(mac).hexdigest().thenReturn('digest')
        when(mac).hexverify(...).thenReturn(None)
        when(mac).hexverify('digest_fail').thenRaise(ValueError)

        when(self._cryptodome_poly1305).new(...).thenReturn(mac)
        when(self._cryptodome_poly1305).new(key=b'key', nonce=b'nonce', cipher=AES, data=ANY).thenReturn(mac)
        when(self._cryptodome_poly1305).new(key=b'key', nonce=b'nonce_fail', cipher=AES, data=ANY).thenRaise(ValueError)

        self._subject = MessageSigner(
            cryptographic_key_deriver=self._cryptographic_key_deriver,
            cryptodome_poly1305=self._cryptodome_poly1305,
        )

    def teardown_method(self):
        """ Resets mocks """
        unstub()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, MessageSigner)

    def test_sign(self):
        """ it signs a given message """
        digest, nonce = self._subject.sign('message')

        assert 'digest' == digest
        assert b'nonce'.hex() == nonce

    def test_verify_sign1(self):
        """ it raises an error when a nonce is incorrect """
        with pytest.raises(StateSignatureCannotBeVerified) as error:
            self._subject.verify_sign('message_fail', b'nonce_fail'.hex(), 'digest')

        assert 'State integrity failed' in str(error)

    def test_verify_sign2(self):
        """ it raises an error when a signature does not match the given message """
        with pytest.raises(StateSignatureCannotBeVerified) as error:
            self._subject.verify_sign('message', b'nonce'.hex(), 'digest_fail')

        assert 'State integrity failed' in str(error)

    def test_verify_sign3(self):
        """ it verifies a message is correct """
        assert self._subject.verify_sign('message', b'nonce'.hex(), 'digest')
