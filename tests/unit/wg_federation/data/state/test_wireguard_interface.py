import pytest
from pydantic import SecretStr

from wg_federation.data.state.wireguard_interface import WireguardInterface


class TestWireguardInterface:
    """ Test WireguardInterface class """

    _subject: WireguardInterface = None

    def setup_method(self):
        """ Constructor """
        self._subject = WireguardInterface(
            name='a_name',
            private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
            public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
            shared_psk='xoSmoykbONQY6XfMYMHpcp/ta3x+FPCUOc4/SQfEQ1E=',
            listen_port=35233,
            mtu=68,
            dns=('1.1.1.1',),
            address=('10.10.100.1/24',),
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, WireguardInterface)

    def test_data(self):
        """ it returns its data """
        assert 'a_name' == self._subject.name
        assert '1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=' == self._subject.public_key
        assert 'xoSmoykbONQY6XfMYMHpcp/ta3x+FPCUOc4/SQfEQ1E=' == self._subject.shared_psk.get_secret_value()
        assert not '9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=' == self._subject.private_key
        assert 35233 == self._subject.listen_port
        assert 68 == self._subject.mtu
        assert '1.1.1.1' == str(self._subject.dns[0])
        assert '10.10.100.1/24' == str(self._subject.address[0])
        assert 'NEW' == self._subject.status

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

    def test_check_name(self):
        """ it raises an error when the wireguard interface name is not valid """
        for wrong_name in [
            'not a valid name',
            '*invalid_federation',
            '',
            'this_is_a_name_too_long-this_is_a_name_too_long-this_is_a_name_too_long-this_is_a_name_too_long-this_is_t',
        ]:
            with pytest.raises(ValueError):
                WireguardInterface(
                    private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
                    name=wrong_name,
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
                public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
                shared_psk='Oh4sAyz3cjJtAAa8thXqZIuLJiy4NFVHSpOfrOM9kn4=',
            )
        assert 'private key, public key and psk must be different from each others' in str(error)

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

    def test_check_psk(self):
        """ it raises an error when the public key is not valid """
        for wrong_psk in [
            'nota_valid_psk',
            SecretStr('test'),
            '*invalid_key',
            'L9kYW/Kej96/L4A???????e2lK5X46gJMfrplRAY4WbK0w4iYRE=',
        ]:
            with pytest.raises(ValueError):
                WireguardInterface(
                    shared_psk=wrong_psk,
                    private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
                )

    def test_from_dict(self):
        """ it instantiates itself using a dict of values """
        assert isinstance(WireguardInterface.from_dict({
            'public_key': '1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
            'private_key': '9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
            'psk': 'v3513CYaiFXqcPoqRgj28GT4tCTcnSO/ywUQM/e1104=',
        }), WireguardInterface)

    def test_from_list(self):
        """ it instantiates itself using a list of dicts of values """
        assert isinstance(WireguardInterface.from_list([{
            'public_key': '1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
            'private_key': '9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
            'psk': 'v3513CYaiFXqcPoqRgj28GT4tCTcnSO/ywUQM/e1104=',
        }, {
            'name': 'a_name',
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
                'Address': '10.10.100.1/24',
                'ListenPort': 35233,
                'MTU': 68,
                'DNS': '1.1.1.1'
            }
        } == self._subject.into_wireguard_ini()
