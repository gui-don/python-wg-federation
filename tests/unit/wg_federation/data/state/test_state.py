import pytest

from wg_federation.data.state.federation import Federation
from wg_federation.data.state.state import State
from wg_federation.data.state.wireguard_interface import WireguardInterface


class TestState:
    """ Test State class """

    _subject: State = None

    def setup(self):
        """ Constructor """
        self._subject = State(
            federation=Federation(name='a_name'),
            interfaces={'test': WireguardInterface(
                private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
            )}
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, State)

    def test_data(self):
        """ it returns its data """
        assert 'a_name' == self._subject.federation.name
        assert 'wg-federation0' == self._subject.interfaces.get('test').name

    def test_check_interface_unique(self):
        """ it raises an error when two interfaces have the same names """
        with pytest.raises(ValueError) as error:
            State(
                federation=Federation(name='a_name'),
                interfaces={'test': WireguardInterface(
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                ), 'test2': WireguardInterface(
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                )}
            )
        assert 'the same name of another interface' in str(error.value)

    def test_check_interface_unique2(self):
        """ it raises an error when two interfaces addresses overlaps """
        with pytest.raises(ValueError) as error:
            State(
                federation=Federation(name='a_name'),
                interfaces={'test': WireguardInterface(
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                    addresses=('192.168.0.0/16',)

                ), 'test2': WireguardInterface(
                    name='fed2',
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                    addresses=('192.168.50.0/24',)
                )}
            )
        assert 'overlaps with another address' in str(error.value)

    def test_check_interface_unique3(self):
        """ it raises an error when two interfaces shares the same listen port """
        with pytest.raises(ValueError) as error:
            State(
                federation=Federation(name='a_name'),
                interfaces={'test': WireguardInterface(
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                    addresses=('192.168.50.0/24',),
                    listen_port=5000
                ), 'test2': WireguardInterface(
                    name='fed2',
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                    addresses=('192.168.100.0/24',),
                    listen_port=5000
                )}
            )
        assert 'has the same listen_port' in str(error.value)

    def test_check_interface_unique4(self):
        """ it raises an error when an interface’s listen port is within the forum range """
        with pytest.raises(ValueError) as error:
            State(
                federation=Federation(name='a_name', forum_max_port=5100, forum_min_port=5000),
                interfaces={'test': WireguardInterface(
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                    listen_port=5050
                )}
            )
        assert 'within the range of the forum ports' in str(error.value)

    def test_check_interface_unique5(self):
        """ it raises an error when an interface’s listen port is within the phone line range """
        with pytest.raises(ValueError) as error:
            State(
                federation=Federation(name='a_name', phone_line_max_port=5100, phone_line_min_port=5000),
                interfaces={'test': WireguardInterface(
                    private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
                    listen_port=5050
                )}
            )
        assert 'within the range of the phone line ports' in str(error.value)

    def test_to_yaml_ready_dict(self):
        """ it exposes itself as a dict ready to be converted to YAML """
        assert 'a_name' == self._subject.to_yaml_ready_dict().get('federation').get('name')
