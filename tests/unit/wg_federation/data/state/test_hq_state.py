import pytest

from unit.wg_federation import hq_state, wireguard_configuration_valid1, wireguard_configuration_valid2, \
    wireguard_configuration_valid3
from wg_federation.data.state.federation import Federation
from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.interface_kind import InterfaceKind
from wg_federation.data.state.wireguard_configuration import WireguardConfiguration
from wg_federation.data.state.wireguard_interface import WireguardInterface


class TestState:
    """ Test State class """

    _subject: HQState = None

    def setup_method(self):
        """ Constructor """
        self._subject = hq_state()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, HQState)

    def test_data(self):
        """ it returns its data """
        assert 'a_name' == self._subject.federation.name
        assert 'wg-federation0' == self._subject.interfaces[0].name
        assert 'qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=' == self._subject.forums[0].interface.public_key
        assert 44100 == self._subject.phone_lines[0].interface.listen_port

    def test_check_interface_unique(self):
        """ it raises an error when two configurations have the same names """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(wireguard_configuration_valid1(), wireguard_configuration_valid1()),
                forums=(wireguard_configuration_valid2(),),
                phone_lines=(wireguard_configuration_valid3(),)
            )
        assert 'the same name of another interface' in str(error.value)

    def test_check_interface_unique2(self):
        """ it raises an error when two interfaces addresses overlaps """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(wireguard_configuration_valid1(),),
                forums=(wireguard_configuration_valid2(),),
                phone_lines=(WireguardConfiguration(
                    name='phone_lines0',
                    interface=WireguardInterface(
                        private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                        public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                        address=(('10.10.0.1/16',)),  # This overlaps with forum address
                    )
                ),)
            )
        assert 'overlaps with another address' in str(error.value)

    def test_check_interface_unique3(self):
        """ it raises an error when two interfaces shares the same listen port """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(WireguardConfiguration(
                    interface=WireguardInterface(
                        public_key='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
                        private_key='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
                        listen_port=44200,  # Same port as forum
                    ),
                    kind=InterfaceKind.INTERFACE,
                ),),
                forums=(wireguard_configuration_valid2(),),
                phone_lines=(wireguard_configuration_valid3(),)
            )
        assert 'has the same listen_port' in str(error.value)

    def test_check_interface_unique4(self):
        """ it raises an error when an interface’s listen port is within the forum range """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(wireguard_configuration_valid1(),),
                forums=(wireguard_configuration_valid2(),),
                phone_lines=(WireguardConfiguration(
                    name='phone_lines0',
                    interface=WireguardInterface(
                        private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                        public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                        address=(('10.10.200.1/24',)),
                        listen_port=44201,  # Not within the phone line range
                    )
                ),)
            )

        assert 'Make sure the port is in the allowed range and not the same' in str(error.value)

    def test_check_interface_unique5(self):
        """ it raises an error when an interface’s listen port is within the phone line range """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(wireguard_configuration_valid1(),),
                forums=(WireguardConfiguration(
                    interface=WireguardInterface(
                        private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                        public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                        address=(('10.10.10.1/24',)),
                        listen_port=44110,  # Within the phone line range
                    ),
                    name='forum0',
                    kind=InterfaceKind.FORUM,
                ),),
                phone_lines=(wireguard_configuration_valid3(),)
            )

        assert 'Make sure the port is in the allowed range and not the same' in str(error.value)

    def test_check_interface_unique6(self):
        """ it raises an error when a forum’s listen port is not within the forums range """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(wireguard_configuration_valid1(),),
                forums=(WireguardConfiguration(
                    interface=WireguardInterface(
                        private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                        public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                        address=(('10.10.10.1/24',)),
                        listen_port=54110,  # Not within the allowed forum range
                    ),
                    name='forum0',
                    kind=InterfaceKind.FORUM,
                ),),
                phone_lines=(wireguard_configuration_valid3(),)
            )

        assert 'Make sure the port is in the allowed range and not the same' in str(error.value)

    def test_check_interface_unique7(self):
        """ it raises an error when a phone line’s listen port is not within the phone line range """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(wireguard_configuration_valid1(),),
                forums=(wireguard_configuration_valid2(),),
                phone_lines=(WireguardConfiguration(
                    name='phone_lines0',
                    interface=WireguardInterface(
                        private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                        public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                        address=(('10.10.200.1/24',)),
                        listen_port=54201,  # Not within the allowed phone line range
                    )
                ),)
            )

        assert 'Make sure the port is in the allowed range and not the same' in str(error.value)

    def test_find_interfaces_by_kind(self):
        """ it returns interfaces based on a given kind """
        assert () == self._subject.find_interfaces_by_kind('does not exists')
        assert InterfaceKind.INTERFACE == self._subject.find_interfaces_by_kind(InterfaceKind.INTERFACE)[0].kind
        assert InterfaceKind.PHONE_LINE == self._subject.find_interfaces_by_kind(InterfaceKind.PHONE_LINE)[0].kind
        assert InterfaceKind.FORUM == self._subject.find_interfaces_by_kind(InterfaceKind.FORUM)[0].kind

    def test_find_interfaces_by_name(self):
        """ it returns interfaces based on a given name and kind """
        assert not self._subject.find_interface_by_name('does not exists', 'nope')
        assert InterfaceKind.FORUM == self._subject.find_interface_by_name(InterfaceKind.FORUM, 'forum0').kind
        assert not self._subject.find_interface_by_name(InterfaceKind.FORUM, 'does not exist')
