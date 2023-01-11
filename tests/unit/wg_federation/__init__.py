from wg_federation.data.state.federation import Federation
from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.interface_kind import InterfaceKind
from wg_federation.data.state.wireguard_interface import WireguardInterface


# pylint: disable=duplicate-code

def hq_state() -> HQState:
    """ Provides a dummy HQState """
    return HQState(
        federation=Federation(name='a_name'),
        interfaces=(WireguardInterface(
            public_key='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
            private_key='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
            shared_psk='mwn0Dfc4IwYlq/jDL08f9VTCM+mQbV2tJlRdIDAy5CA=',
            kind=InterfaceKind.INTERFACE,
        ),),
        forums=(WireguardInterface(
            name='forum0',
            private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
            public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
            address=(('10.10.10.1/24',)),
            listen_port=44200,
            kind=InterfaceKind.FORUM,
        ),),
        phone_lines=(WireguardInterface(
            name='phone_lines0',
            private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
            public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
            address=(('10.10.200.1/24',)),
            listen_port=44100,
            kind=InterfaceKind.PHONE_LINE,
        ),)
    )
