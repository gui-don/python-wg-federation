import pytest

from unit.wg_federation import wireguard_configuration_valid3, wireguard_interface_valid1, \
    wireguard_configuration_valid2
from wg_federation.data.state.interface_kind import InterfaceKind
from wg_federation.data.state.wireguard_configuration import WireguardConfiguration
from wg_federation.data.state.wireguard_interface import WireguardInterface


class TestWireguardConfiguration:
    """ Test WireguardConfiguration class """

    _subject: WireguardConfiguration = None

    def setup_method(self):
        """ Constructor """
        self._subject = wireguard_configuration_valid3()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, WireguardConfiguration)

    def test_data(self):
        """ it returns its data """
        assert isinstance(self._subject.interface, WireguardInterface)
        assert 'phone_lines0' == self._subject.name
        assert 'aLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=' == self._subject.shared_psk.get_secret_value()
        assert 'NEW' == self._subject.status
        assert InterfaceKind.PHONE_LINE == self._subject.kind

    def test_check_shared_psk1(self):
        """ it raises an error if the pre-shared key is not a valid WireGuard shared key """
        for wrong_key in [
            'not a valid name',
            '*invalid_key',
            'L9kYW/Kej96/L4A???????e2lK5X46gJMfrplRAY4WbK0w4iYRE=',
        ]:
            with pytest.raises(ValueError) as error:
                WireguardConfiguration(
                    interface=wireguard_interface_valid1(),
                    shared_psk=wrong_key,
                    kind=InterfaceKind.INTERFACE,
                )

            assert 'WireGuard configuration was provided an invalid Pre-Shared key.' in str(error)

    def test_check_shared_psk2(self):
        """ it raises an error if the pre-shared key is the same as the interface public key """
        with pytest.raises(ValueError) as error:
            WireguardConfiguration(
                interface=wireguard_interface_valid1(),
                shared_psk='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
                kind=InterfaceKind.INTERFACE,
            )

        assert 'private key, public key and psk must be different from each others' in str(error)

    def test_check_shared_psk3(self):
        """ it raises an error if the pre-shared key is the same as the interface private key """
        with pytest.raises(ValueError) as error:
            WireguardConfiguration(
                interface=wireguard_interface_valid1(),
                shared_psk='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
                kind=InterfaceKind.INTERFACE,
            )

        assert 'private key, public key and psk must be different from each others' in str(error)

    def test_from_dict(self):
        """ it instantiates itself using a dict of values """
        subject = WireguardConfiguration.from_dict(wireguard_configuration_valid3().dict(exclude_defaults=True))

        assert isinstance(subject.interface, WireguardInterface)
        assert 'phone_lines0' == subject.name
        assert 'aLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=' == subject.shared_psk.get_secret_value()
        assert 'NEW' == subject.status
        assert InterfaceKind.PHONE_LINE == subject.kind

    def test_from_list(self):
        """ it instantiates itself using a list of dicts of values """
        subject = WireguardConfiguration.from_list([
            wireguard_configuration_valid3().dict(exclude_defaults=True),
            wireguard_configuration_valid2().dict(exclude_defaults=True)
        ])

        assert isinstance(subject[0].interface, WireguardInterface)
        assert 'phone_lines0' == subject[0].name
        assert 'aLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=' == subject[0].shared_psk.get_secret_value()
        assert 'NEW' == subject[0].status
        assert InterfaceKind.PHONE_LINE == subject[0].kind

        assert isinstance(subject[1].interface, WireguardInterface)
        assert 'forum0' == subject[1].name
        assert not subject[1].shared_psk
        assert 'NEW' == subject[0].status
        assert InterfaceKind.FORUM == subject[1].kind

    def test_into_wireguard_ini(self):
        """ it gives a view of itself as wireguard ini-ready dict  """
        # pylint: disable=duplicate-code
        assert [{
            'Interface': {
                'Address': '10.10.200.1/24',
                'ListenPort': 44100,
                'MTU': 1300,
                'DNS': '1.1.1.1, 2001:4860:4860::8888'
            }
        }, {
            'Peer': {
                'AllowedIPs': '10.10.100.0/24',
                'Endpoint': 'test.default.com:35200',
                'PersistentKeepalive': 30,
                'PublicKey': 'ACiLCMkq2amL/onCQHFHTV9HxRiyP0gCeGohZwGaXkI='
            }}, {
            'Peer': {
                'AllowedIPs': '10.10.100.0/24, 172.16.24.43/32',
                'Endpoint': 'test.default.com:44243',
                'PresharedKey': '8KepxYN1YTlxV9pbEWgkyxZjzhqsP7QHZ7AEKghVyVM=',
                'PublicKey': '+G4a/5OtIiIxBml0GWOc5RBFyZBVPD/Awzi6R+89imY='}
        }, ] == self._subject.into_wireguard_ini()
