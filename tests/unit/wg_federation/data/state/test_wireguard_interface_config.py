import pytest

from wg_federation.data.state.wireguard_interface import WireguardInterface


class TestWireguardInterfaceConfig:
    """ Test WireguardInterfaceConfig class """

    _subject: WireguardInterface = None

    def setup(self):
        """ Constructor """
        self._subject = WireguardInterface(
            name='a_name',
            private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
            public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
            listen_port=35233,
            mtu=68,
            dns=('1.1.1.1',),
            addresses=('10.10.100.1/24',),
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, WireguardInterface)

    def test_data(self):
        """ it returns its data """
        assert 'a_name' == self._subject.name
        assert 'L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=' == self._subject.public_key
        assert not 'L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=' == self._subject.private_key
        assert 35233 == self._subject.listen_port
        assert 68 == self._subject.mtu
        assert '1.1.1.1' == str(self._subject.dns[0])
        assert '10.10.100.1/24' == str(self._subject.addresses[0])

    def test_to_yaml_ready_dict(self):
        """ it exposes itself as a dict ready to be converted to YAML """
        assert '10.10.100.1/24' == self._subject.to_yaml_ready_dict().get('addresses')[0]

    def test_addresses(self):
        """ it raises one of the addresses is not a valid address """
        with pytest.raises(ValueError):
            WireguardInterface(
                private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                addresses=('fails',),
            )

    def test_dns(self):
        """ it raises one of the DNS is not a valid IP """
        with pytest.raises(ValueError):
            WireguardInterface(
                private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                dns=('1.1.1.1', 'not_ip',),
            )

    def test_listen_port(self):
        """ it raises an error if listen port is higher than 65535 """
        with pytest.raises(ValueError):
            WireguardInterface(
                private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                listen_port=75000,
            )

    def test_mtu1(self):
        """ it raises an error if MTU is less than 68 """
        with pytest.raises(ValueError):
            WireguardInterface(
                private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                mtu=50,
            )

    def test_mtu2(self):
        """ it raises an error if MTU is more than 65535 """
        with pytest.raises(ValueError):
            WireguardInterface(
                private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
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
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
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
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key=wrong_key,
                )

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
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                )
