from wg_federation.data.state.federation import Federation
from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.interface_kind import InterfaceKind
from wg_federation.data.state.wireguard_configuration import WireguardConfiguration
from wg_federation.data.state.wireguard_interface import WireguardInterface
from wg_federation.data.state.wireguard_peer import WireguardPeer


# pylint: disable=duplicate-code

def wireguard_interface_valid1() -> WireguardInterface:
    """ Provides a dummy WireguardInterface """

    return WireguardInterface(
        public_key='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
        private_key='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
    )


def wireguard_interface_valid2() -> WireguardInterface:
    """ Provides a dummy WireguardInterface """

    return WireguardInterface(
        private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
        public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
        address=(('10.10.10.1/24',)),
        listen_port=44200,
    )


def wireguard_interface_valid3() -> WireguardInterface:
    """ Provides a dummy WireguardInterface """

    return WireguardInterface(
        private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
        public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
        address=(('10.10.200.1/24',)),
        dns=('1.1.1.1', '2001:4860:4860::8888'),
        listen_port=44100,
        mtu=1300,
    )


def wireguard_configuration_valid1() -> WireguardConfiguration:
    """ Provides a valid WireguardConfiguration """

    return WireguardConfiguration(
        interface=wireguard_interface_valid1(),
        shared_psk='mwn0Dfc4IwYlq/jDL08f9VTCM+mQbV2tJlRdIDAy5CA=',
        kind=InterfaceKind.INTERFACE,
    )


def wireguard_configuration_valid2() -> WireguardConfiguration:
    """ Provides a valid, semi-complex WireguardConfiguration """

    return WireguardConfiguration(
        interface=wireguard_interface_valid2(),
        peers=(wireguard_peer_valid1(),),
        name='forum0',
        kind=InterfaceKind.FORUM,
    )


def wireguard_configuration_valid3() -> WireguardConfiguration:
    """ Provides a valid, complex WireguardConfiguration """

    return WireguardConfiguration(
        interface=wireguard_interface_valid3(),
        peers=(wireguard_peer_valid2(), wireguard_peer_valid3()),
        name='phone_lines0',
        shared_psk='aLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
        kind=InterfaceKind.PHONE_LINE,
    )


def wireguard_peer_valid1() -> WireguardPeer:
    """ Provides a valid WireguardPeer """

    return WireguardPeer(
        public_key='kAu4UJK7JyagWmpXujSAZQzxxcRX6383CaKfppyl/lk='
    )


def wireguard_peer_valid2() -> WireguardPeer:
    """ Provides a valid, semi-complex WireguardPeer """

    return WireguardPeer(
        public_key='ACiLCMkq2amL/onCQHFHTV9HxRiyP0gCeGohZwGaXkI=',
        endpoint_host='test.default.com',
        persistent_keep_alive=30,
    )


def wireguard_peer_valid3() -> WireguardPeer:
    """ Provides a valid, complex WireguardPeer """
    return WireguardPeer(
        public_key='+G4a/5OtIiIxBml0GWOc5RBFyZBVPD/Awzi6R+89imY=',
        pre_shared_key='8KepxYN1YTlxV9pbEWgkyxZjzhqsP7QHZ7AEKghVyVM=',
        allowed_ips=('10.10.100.0/24', '172.16.24.43/32'),
        endpoint_host='test.default.com',
        endpoint_port=44243,
    )


def hq_state() -> HQState:
    """ Provides a dummy HQState """
    return HQState(
        federation=Federation(name='a_name'),
        interfaces=(wireguard_configuration_valid1(),),
        forums=(wireguard_configuration_valid2(),),
        phone_lines=(wireguard_configuration_valid3(),),
    )
