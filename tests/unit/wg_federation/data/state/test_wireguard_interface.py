import pytest
from mockito import unstub

from unit.wg_federation import wireguard_interface_valid3
from wg_federation.data.state.wireguard_interface import WireguardInterface


class TestWireguardInterface:
    """ Test WireguardInterface class """

    _subject: WireguardInterface = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """
        self._subject = wireguard_interface_valid3()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, WireguardInterface)

    def test_data(self):
        """ it returns its data """
        assert 'nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=' == self._subject.public_key
        assert 'mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=' == self._subject.private_key.get_secret_value()
        assert not 'mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=' == self._subject.private_key
        assert 44100 == self._subject.listen_port
        assert 1300 == self._subject.mtu
        assert '1.1.1.1' == str(self._subject.dns[0])
        assert '2001:4860:4860::8888' == str(self._subject.dns[1])
        assert '10.10.200.1/24' == str(self._subject.address[0])

    def test_addresses(self):
        """ it raises one of the addresses is not a valid address """
        with pytest.raises(ValueError):
            WireguardInterface(
                public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
                private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                shared_psk='v3513CYaiFXqcPoqRgj28GT4tCTcnSO/ywUQM/e1104=',
                address=('fails',),
            )

    def test_dns(self):
        """ it raises one of the DNS is not a valid IP """
        with pytest.raises(ValueError):
            WireguardInterface(
                private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
                dns=('1.1.1.1', 'not_ip',),
            )

    def test_listen_port(self):
        """ it raises an error if listen port is higher than 65535 """
        with pytest.raises(ValueError):
            WireguardInterface(
                public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
                private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                listen_port=75000,
            )

    def test_mtu1(self):
        """ it raises an error if MTU is less than 68 """
        with pytest.raises(ValueError):
            WireguardInterface(
                private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
                mtu=50,
            )

    def test_mtu2(self):
        """ it raises an error if MTU is more than 65535 """
        with pytest.raises(ValueError):
            WireguardInterface(
                private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
                mtu=70535,
            )

    def test_check_public_key(self):
        """ it raises an error when the public key is not valid """
        for wrong_key in [
            'not a valid name',
            '*invalid_key',
            'L9kYW/Kej96/L4A???????e2lK5X46gJMfrplRAY4WbK0w4iYRE=',
        ]:
            with pytest.raises(ValueError):
                WireguardInterface(
                    private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key=wrong_key,
                )

        with pytest.raises(ValueError) as error:
            WireguardInterface(
                private_key='Oh4sAyz3cjJtAAa8thXqZIuLJiy4NFVHSpOfrOM9kn4=',
                public_key='Oh4sAyz3cjJtAAa8thXqZIuLJiy4NFVHSpOfrOM9kn4=',
            )
        assert 'A WireGuard interface have the same public and private key' in str(error)

    def test_check_private_key(self):
        """ it raises an error when the public key is not valid """
        for wrong_key in [
            'not a valid name',
            '*invalid_key',
            'L9kYW/Kej96/L4A???????e2lK5X46gJMfrplRAY4WbK0w4iYRE=',
        ]:
            with pytest.raises(ValueError):
                WireguardInterface(
                    private_key=wrong_key,
                    public_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                )

    def test_from_dict(self):
        """ it instantiates itself using a dict of values """
        assert isinstance(WireguardInterface.from_dict({
            'public_key': '1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
            'psk': 'v3513CYaiFXqcPoqRgj28GT4tCTcnSO/ywUQM/e1104=',
        }), WireguardInterface)

    def test_from_list(self):
        """ it instantiates itself using a list of dicts of values """
        assert isinstance(WireguardInterface.from_list([{
            'public_key': '1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
            'private_key': '9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
        }, {
            'private_key': '9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
            'public_key': '1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
            'psk': 'xoSmoykbONQY6XfMYMHpcp/ta3x+FPCUOc4/SQfEQ1E=',
            'listen_port': 35233,
            'address': ('10.10.100.1/24',),
        }]), tuple)

    def test_into_wireguard_ini(self):
        """ it gives a view of itself as wireguard ini-ready dict  """
        assert {
            'Interface': {
                'Address': '10.10.200.1/24',
                'ListenPort': 44100,
                'MTU': 1300,
                'DNS': '1.1.1.1, 2001:4860:4860::8888'
            }
        } == self._subject.into_wireguard_ini()
