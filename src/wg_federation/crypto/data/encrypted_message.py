from pydantic import BaseModel


# mypy: ignore-errors
# https://github.com/pydantic/pydantic/issues/156


class EncryptedMessage(BaseModel, frozen=True):
    """
    Data class for an encrypted message
    """

    ciphertext: bytes = None
    digest: bytes = None
    nonce: bytes = None

    def get_hex_ciphertext(self) -> str:
        """
        Get ciphertext in hexadecimal format
        :return:
        """
        return self.ciphertext.hex()

    def get_hex_digest(self) -> str:
        """
        Get digest in hexadecimal format
        :return:
        """
        return self.digest.hex()

    def get_hex_nonce(self) -> str:
        """
        Get nonce in hexadecimal format
        :return:
        """
        return self.nonce.hex()
