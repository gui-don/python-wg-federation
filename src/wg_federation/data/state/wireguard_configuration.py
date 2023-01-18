import re
from typing import Any

from pydantic import BaseModel, SecretStr, constr, validator

from wg_federation.constants import REGEXP_WIREGUARD_KEY
from wg_federation.data.state.interface_kind import InterfaceKind
from wg_federation.data.state.interface_status import InterfaceStatus
from wg_federation.data.state.wireguard_interface import WireguardInterface
from wg_federation.data.state.wireguard_peer import WireguardPeer
from wg_federation.exception.developer.data.data_validation_error import DataValidationError


# mypy: ignore-errors
# https://github.com/pydantic/pydantic/issues/156

class WireguardConfiguration(BaseModel, frozen=True):
    """
    Data class representing a WireGuard configuration file
    """

    _REGEXP_WIREGUARD_INTERFACE_NAME = r'^[a-zA-Z0-9_=+-]{1,15}$'

    interface: WireguardInterface
    peers: tuple[WireguardPeer, ...] = ()

    name: constr(regex=_REGEXP_WIREGUARD_INTERFACE_NAME) = 'wg-federation0'
    status: InterfaceStatus = InterfaceStatus.NEW
    kind: InterfaceKind = None
    shared_psk: SecretStr = None

    # pylint: disable=no-self-argument
    @validator('shared_psk')
    def check_shared_psk(cls, value: SecretStr, values: dict) -> SecretStr:
        """
        Validate psk.
        Also validate psk, public_key and private_key relation together.
        :param value: psk value
        :param values: rest of the current object’s attributes
        :return:
        """
        if not re.match(REGEXP_WIREGUARD_KEY, value.get_secret_value()):
            raise DataValidationError(
                f'The “{values.get("name")}” WireGuard configuration was provided an invalid Pre-Shared key.'
            )

        cls._check_public_private_and_psk(
            values.get('interface').public_key,
            values.get('interface').private_key.get_secret_value(),
            value.get_secret_value(),
            values.get('name')
        )

        return value

    @classmethod
    def from_dict(cls, configuration: dict[str, Any]) -> 'WireguardConfiguration':
        """
        Create a new WireguardConfiguration from a dict of key/values.
        :param configuration:
        :return: WireguardConfiguration
        """
        return cls(**configuration)

    @classmethod
    def from_list(cls, configurations: list[dict[str, Any]]) -> tuple['WireguardConfiguration', ...]:
        """
        Instantiate a tuple of WireguardConfiguration using a list of dict of keys/values
        :param configurations:
        :return: tuple of WireguardConfiguration
        """
        return tuple(map(cls.from_dict, configurations))

    def into_wireguard_ini(self) -> list:
        """
        Transform the current object into a dict specifically made for WireGuard configuration files
        :return:
        """

        return [self.interface.into_wireguard_ini()] + [peer.into_wireguard_ini() for peer in self.peers]

    @classmethod
    def _check_public_private_and_psk(cls, public_key: str, private_key: str, psk: str, interface_name: str) -> None:
        if len({public_key}.union({private_key}).union({psk})) != 3:
            raise DataValidationError(
                f'The WireGuard configuration named “{interface_name}”'
                f'private key, public key and psk must be different from each others.'
            )
