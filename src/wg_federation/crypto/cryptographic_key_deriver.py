import argparse
import functools
import os
from functools import _CacheInfo

import xdg
from Cryptodome.Hash import SHA512
from Cryptodome.Protocol import KDF
from pydantic import SecretStr

from wg_federation.data.input.user_input import UserInput
from wg_federation.exception.developer.crypto.root_passphrase_not_set import RootPassphraseNotSet
from wg_federation.exception.developer.crypto.salt_file_not_found import SaltFileNotFound


class CryptographicKeyDeriver:
    """
    Able to derive cryptographic keys.
    """

    SALT_FILENAME = 'passphrase.salt'

    _user_input: UserInput = None

    def __init__(self, user_input: UserInput):
        """
        Constructor
        :param user_input:
        """
        self._user_input = user_input

    @functools.lru_cache(maxsize=8, typed=False)
    def derive_32b_key_from_root_passphrase(self) -> bytes:
        """
        Derive a 32byte cryptographic key from the current root passphrase.
        As deriving a key can impact performance, the result of this function is cached.
        :return: 32b key
        """
        return KDF.PBKDF2(
            password=self._get_root_passphrase(),
            salt=self._get_salt_from_file().encode('UTF-8'),
            dkLen=32,
            count=1111,
            hmac_hash_module=SHA512
        )

    def clear_cache(self) -> None:
        """
        Clear the cache for all this class’s functions
        :return: None
        """
        self.derive_32b_key_from_root_passphrase.cache_clear()

    def get_cache_status(self) -> _CacheInfo:
        """
        Return cache information
        :return: CacheInfo
        """
        return self.derive_32b_key_from_root_passphrase.cache_info()

    def get_salt_full_path(self) -> str:
        """
        Returns the full path of the salt file
        :return:
        """
        return os.path.join(xdg.xdg_data_home(), argparse.ArgumentParser().prog, self.SALT_FILENAME)

    def _get_salt_from_file(self) -> str:
        try:
            with open(self.get_salt_full_path(), 'r', encoding='UTF-8') as file_handler:
                return file_handler.read()
        except FileNotFoundError as error:
            raise SaltFileNotFound(
                f'Salt file {self.get_salt_full_path()} cannot be found.{os.linesep}'
                f'Original error: {error}.'
            ) from error

    def _get_root_passphrase(self) -> str:
        if not isinstance(self._user_input.root_passphrase, SecretStr) or\
                not self._user_input.root_passphrase.get_secret_value():
            raise RootPassphraseNotSet(
                'Cannot derive cryptographic key. The root passphrase was not set.'
            )

        return self._user_input.root_passphrase.get_secret_value()
