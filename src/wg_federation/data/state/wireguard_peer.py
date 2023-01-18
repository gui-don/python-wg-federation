import re
from typing import Any, Optional

from pydantic import BaseModel, conint, constr, IPvAnyInterface, SecretStr, validator
from pydantic.networks import _host_regex

from wg_federation.constants import REGEXP_WIREGUARD_KEY
from wg_federation.exception.developer.data.data_validation_error import DataValidationError


# mypy: ignore-errors
# https://github.com/pydantic/pydantic/issues/156


class WireguardPeer(BaseModel, frozen=True):
    """
    Data class representing a WireGuard peer
    """

    public_key: constr(regex=REGEXP_WIREGUARD_KEY)
    pre_shared_key: SecretStr = None
    allowed_ips: tuple[IPvAnyInterface, ...] = ('10.10.100.0/24',)
    endpoint_host: Optional[constr(regex=_host_regex)] = None
    endpoint_port: conint(ge=1, le=65535) = 35200
    persistent_keep_alive: Optional[conint(ge=1, le=65535)] = None

    # pylint: disable=no-self-argument
    @validator('pre_shared_key')
    def pre_shared_key_is_valid(cls, value: SecretStr, values: dict) -> SecretStr:
        """ Validates the pre_shared_key """
        if not re.match(REGEXP_WIREGUARD_KEY, value.get_secret_value()):
            raise DataValidationError('A pre-shared key in a WireGuard peer is invalid.')

        if value.get_secret_value() == values.get('public_key'):
            raise DataValidationError('A WireGuard peer got the same public and pre-shared key.')

        return value

    @classmethod
    def from_dict(cls, configuration: dict[str, Any]) -> 'WireguardPeer':
        """
        Create a new WireguardPeer from a dict of key/values.
        :param configuration:
        :return: WireguardPeer
        """
        return cls(**configuration)

    def into_wireguard_ini(self) -> dict:
        """
        Transform the current object into a dict specifically made for WireGuard configuration files
        :return:
        """

        # While this is manual and inconvenient, unfruitful research was done:
        # - Use pydentic aliases for keys: buggy, mess with IDE static analysis
        # - Using configparse: wireguard needs duplicated section, not handled by configparser
        # - Using toml: wireguard configuration is not toml compliant
        return {
            'Peer': self.copy(
                include={},
                update={
                    'PublicKey': self.public_key,
                    'PresharedKey': self.pre_shared_key.get_secret_value() if self.pre_shared_key else None,
                    'AllowedIPs': ', '.join(str(allowed_ip) for allowed_ip in self.allowed_ips),
                    'Endpoint': f'{self.endpoint_host}:{self.endpoint_port}' if self.endpoint_host else None,
                    'PersistentKeepalive': self.persistent_keep_alive if self.persistent_keep_alive else None,
                }).dict(exclude_none=True, )
        }
