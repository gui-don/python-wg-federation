import re

from pydantic import BaseModel, IPvAnyAddress, conint, constr, IPvAnyInterface, SecretStr, validator

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

    private_key: SecretStr
    public_key: constr(regex=_REGEXP_WIREGUARD_KEY)

    @classmethod
    @validator('private_key')
    def check_forum_min_port(cls, value: SecretStr, values: dict) -> SecretStr:
        """
        Validate private_key
        :param value: private_key value
        :param values: rest of the current object’s attributes
        :return:
        """
        if not re.match(cls._REGEXP_WIREGUARD_KEY, value.get_secret_value()):
            raise ValueError(f'The interface {values.get("name")} was provided an invalid private key.')

        return value

    def to_yaml_ready_dict(self) -> dict:
        """
        Return a dict version of this object, ready to be serialized in a configuration file
        :return:
        """
        return dict(self.copy(exclude={'server_private_key'}, update={
            'addresses': [str(address) for address in self.addresses],
            'dns': [str(dns) for dns in self.dns]
        }))
