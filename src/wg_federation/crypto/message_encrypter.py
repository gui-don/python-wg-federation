from binascii import unhexlify

from Cryptodome.Cipher import AES

from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver


class MessageEncrypter:
    """
    Able to encrypt and decrypt a message.
    """

    _cryptographic_key_deriver = None
    _cryptodome_aes = None

    def __init__(self, cryptographic_key_deriver: CryptographicKeyDeriver, cryptodome_aes: AES):
        """
        Constructor
        :param cryptographic_key_deriver:
        :param cryptodome_aes:
        """
        self._cryptographic_key_deriver = cryptographic_key_deriver
        self._cryptodome_aes = cryptodome_aes

    def encrypt(self, message: bytes) -> dict[str, str]:
        """
        Encrypted a given message
        :param message: Message to encrypt
        :return: dict containing: 'ciphertext' = ciphertext in hex, 'digest' = digest in hex, 'nonce' = nonce in hex
        """
        cipher = self._cryptodome_aes.new(
            key=self._cryptographic_key_deriver.derive_32b_key_from_root_passphrase(),
            mode=AES.MODE_EAX
        )

        ciphertext, digest = cipher.encrypt_and_digest(message)

        return {
            'ciphertext': ciphertext.hex(),
            'digest': digest.hex(),
            'nonce': cipher.nonce.hex()
        }

    def decrypt(self, ciphertext_hex: str, nonce_hex: str, digest_hex: str) -> bytes:
        """
        Decipher a given ciphertext with the nonce and digest
        :param ciphertext_hex: Ciphertext in hexadecimal format
        :param nonce_hex: Nonce used for encryption in hexadecimal format
        :param digest_hex: Digest used for encryption in hexadecimal format
        :return:
        """
        return self._cryptodome_aes.new(
            key=self._cryptographic_key_deriver.derive_32b_key_from_root_passphrase(),
            mode=AES.MODE_EAX,
            nonce=unhexlify(nonce_hex)
        ).decrypt_and_verify(unhexlify(ciphertext_hex), unhexlify(digest_hex))
