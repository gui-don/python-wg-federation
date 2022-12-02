import re

from pydantic import BaseModel, IPvAnyAddress, conint, constr, IPvAnyInterface, SecretStr, validator

from wg_federation.data.state.interface_status import InterfaceStatus


# mypy: ignore-errors
# https://github.com/pydantic/pydantic/issues/156


class WireguardInterface(BaseModel, frozen=True):
    """
    Data class representing a wireguard interface
    """

    _REGEXP_WIREGUARD_KEY = r'^[0-9A-Za-z+/]+[=]$'
    _REGEXP_WIREGUARD_INTERFACE_NAME = r'^[a-zA-Z0-9_=+-]{1,15}$'

    addresses: tuple[IPvAnyInterface] = ('10.10.100.1/24',)
    dns: tuple[IPvAnyAddress] = ()
    listen_port: conint(le=65535) = 35200
    mtu: conint(ge=68, le=65535) = None
    name: constr(regex=_REGEXP_WIREGUARD_INTERFACE_NAME) = 'wg-federation0'
    status: InterfaceStatus = InterfaceStatus.NEW

    private_key: SecretStr
    psk: SecretStr = None
    public_key: constr(regex=_REGEXP_WIREGUARD_KEY)

    # pylint: disable=no-self-argument
    @validator('private_key')
    def check_private_key(cls, value: SecretStr, values: dict) -> SecretStr:
        """
        Validate private_key
        :param value: private_key value
        :param values: rest of the current object’s attributes
        :return:
        """
        return cls._check_wireguard_key(value, values, 'private_key')

    # pylint: disable=no-self-argument
    @validator('psk')
    def check_psk(cls, value: SecretStr, values: dict) -> SecretStr:
        """
        Validate psk
        :param value: psk value
        :param values: rest of the current object’s attributes
        :return:
        """
        return cls._check_wireguard_key(value, values, 'psk')

    @classmethod
    def _check_wireguard_key(cls, value: SecretStr, values: dict, kind: str) -> SecretStr:
        if not re.match(cls._REGEXP_WIREGUARD_KEY, value.get_secret_value()):
            raise ValueError(f'The interface {values.get("name")} was provided an invalid {kind}.')

        return value
