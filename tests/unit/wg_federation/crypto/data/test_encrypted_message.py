from wg_federation.crypto.data.encrypted_message import EncryptedMessage


class TestCommandLineArgument:
    """ Test EncryptedMessage class """

    _subject: EncryptedMessage = None

    def setup_method(self):
        """ Constructor """
        self._subject = EncryptedMessage(
            ciphertext=b'very secret secret',
            digest=b'a_digest',
            nonce=b'a nonce',
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, EncryptedMessage)

    def test_data(self):
        """ it returns its data """
        assert b'very secret secret' == self._subject.ciphertext
        assert b'a_digest' == self._subject.digest
        assert b'a nonce' == self._subject.nonce

    def test_data2(self):
        """ it returns its data in hexadecimal """
        assert b'very secret secret'.hex() == self._subject.get_hex_ciphertext()
        assert b'a_digest'.hex() == self._subject.get_hex_digest()
        assert b'a nonce'.hex() == self._subject.get_hex_nonce()

    def test_hex_dict(self):
        """ it returns itself in a hexadecimal dict """
        assert {
            'ciphertext': b'very secret secret'.hex(),
            'digest': b'a_digest'.hex(),
            'nonce': b'a nonce'.hex(),
        } == self._subject.hex_dict()

    def test_from_hex(self):
        """ it can instantiate itself from hexadecimal values """
        result = EncryptedMessage.from_hex(b'ciphertext'.hex(), b'digest'.hex(), b'nonce'.hex())

        assert isinstance(result, EncryptedMessage)
        assert b'ciphertext' == result.ciphertext
        assert b'digest' == result.digest
        assert b'nonce' == result.nonce
