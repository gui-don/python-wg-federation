import pytest

from unit.wg_federation import wireguard_peer_valid3
from wg_federation.data.state.wireguard_peer import WireguardPeer


class TestWireguardPeer:
    """ Test WireguardPeer class """

    _subject: WireguardPeer = None

    def setup_method(self):
        """ Constructor """
        self._subject = wireguard_peer_valid3()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, WireguardPeer)

    def test_data(self):
        """ it returns its data """
        assert '+G4a/5OtIiIxBml0GWOc5RBFyZBVPD/Awzi6R+89imY=' == self._subject.public_key
        assert '8KepxYN1YTlxV9pbEWgkyxZjzhqsP7QHZ7AEKghVyVM=' == self._subject.pre_shared_key.get_secret_value()
        assert not '8KepxYN1YTlxV9pbEWgkyxZjzhqsP7QHZ7AEKghVyVM=' == self._subject.pre_shared_key
        assert 44243 == self._subject.endpoint_port
        assert 'test.default.com' == self._subject.endpoint_host
        assert not self._subject.persistent_keep_alive

    def test_pre_shared_key_is_valid1(self):
        """ it raises an error if the pre-shared key is not a valid WireGuard shared key """
        for wrong_key in [
            'invalid name',
            'L9AM=',
            '+toolongG4a/5OtIiIxBml0GWOc5RBFyZBVPD/AwzimY=',
        ]:
            with pytest.raises(ValueError) as error:
                WireguardPeer(
                    public_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                    pre_shared_key=wrong_key,
                )

            assert 'A pre-shared key in a WireGuard peer is invalid.' in str(error)

    def test_pre_shared_key_is_valid2(self):
        """ it raises an error if the pre-shared key is the same as the public key """
        with pytest.raises(ValueError) as error:
            WireguardPeer(
                public_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
                pre_shared_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
            )

        assert 'A WireGuard peer got the same public and pre-shared key.' in str(error)

    def test_from_dict(self):
        """ it instantiates itself using a dict of values """
        subject = WireguardPeer.from_dict(wireguard_peer_valid3().dict(exclude_defaults=True))

        assert '+G4a/5OtIiIxBml0GWOc5RBFyZBVPD/Awzi6R+89imY=' == subject.public_key
        assert '8KepxYN1YTlxV9pbEWgkyxZjzhqsP7QHZ7AEKghVyVM=' == subject.pre_shared_key.get_secret_value()
        assert not '8KepxYN1YTlxV9pbEWgkyxZjzhqsP7QHZ7AEKghVyVM=' == subject.pre_shared_key
        assert 44243 == subject.endpoint_port
        assert 'test.default.com' == subject.endpoint_host
        assert not subject.persistent_keep_alive

    def test_into_wireguard_ini(self):
        """ it gives a view of itself as wireguard ini-ready dict  """
        assert {
            'Peer': {
                'PublicKey': '+G4a/5OtIiIxBml0GWOc5RBFyZBVPD/Awzi6R+89imY=',
                'PresharedKey': '8KepxYN1YTlxV9pbEWgkyxZjzhqsP7QHZ7AEKghVyVM=',
                'AllowedIPs': '10.10.100.0/24, 172.16.24.43/32',
                'Endpoint': 'test.default.com:44243'
            }
        } == self._subject.into_wireguard_ini()
