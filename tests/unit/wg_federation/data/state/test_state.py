import pytest

from wg_federation.data.state.federation import Federation
from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.wireguard_interface import WireguardInterface


class TestState:
    """ Test State class """

    _subject: HQState = None

    def setup_method(self):
        """ Constructor """
        self._subject = HQState(
            federation=Federation(name='a_name'),
            interfaces=(WireguardInterface(
                public_key='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
                private_key='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
                shared_psk='mwn0Dfc4IwYlq/jDL08f9VTCM+mQbV2tJlRdIDAy5CA=',
            ),),
            forums=(WireguardInterface(
                name='forum0',
                private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                address=(('10.10.10.1/24',)),
                listen_port=44200,
            ),),
            phone_lines=(WireguardInterface(
                name='phone_lines0',
                private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                address=(('10.10.200.1/24',)),
                listen_port=44100,
            ),)
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, HQState)

    def test_data(self):
        """ it returns its data """
        assert 'a_name' == self._subject.federation.name
        assert 'wg-federation0' == self._subject.interfaces[0].name
        assert 'qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=' == self._subject.forums[0].public_key
        assert 44100 == self._subject.phone_lines[0].listen_port

    def test_check_interface_unique(self):
        """ it raises an error when two interfaces have the same names """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(WireguardInterface(
                    private_key='7mMIFixIzNmbRASMK2QUHUnNNujLvxfL57HHcqMsOxo=',
                    public_key='YIgDvmfnI2BBgoYkCxhnnK3Ja0kDBAKTaKfT09qL6A4=',
                ), WireguardInterface(
                    private_key='5D1jfCDCtzj3TomvcXGPfM3AMpJcAJD26B48wxdTvVU=',
                    public_key='wyj+owdxHy9fJLAoQPOXjVNVfi/f6dzuiFmwAaZAJEc=',
                ),),
                forums=(WireguardInterface(
                    name='forum0',
                    private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                    public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                    address=(('10.10.10.1/24',)),
                    listen_port=44200,
                ),),
                phone_lines=(WireguardInterface(
                    name='phone_lines0',
                    private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                    public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                    address=(('10.10.200.1/24',)),
                    listen_port=44100,
                ),)
            )
        assert 'the same name of another interface' in str(error.value)

    def test_check_interface_unique2(self):
        """ it raises an error when two interfaces addresses overlaps """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(WireguardInterface(
                    private_key='bRdbrR9E1nKXa2g7qkTVSty9GXZ6Vvj9p2TDpEEGLFE=',
                    public_key='MDuAwX+2NvIiYuagR1k5LnM1K3jCp0BB7uZZJB1tPmM=',
                    address=('192.168.0.0/16',)

                ),),
                forums=(WireguardInterface(
                    name='forum0',
                    private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                    public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                    address=('192.168.50.0/24',),
                    listen_port=44200,
                ),),
                phone_lines=(WireguardInterface(
                    name='phone_lines0',
                    private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                    public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                    address=(('10.10.200.1/24',)),
                    listen_port=44100,
                ),)
            )
        assert 'overlaps with another address' in str(error.value)

    def test_check_interface_unique3(self):
        """ it raises an error when two interfaces shares the same listen port """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(WireguardInterface(
                    private_key='Ee862wOc4Fv9ttqUOYCLsTVUQm0kbwdGyq0v8e3cGhs=',
                    public_key='W7ExEOJEEcLFcsf/Y2B4nOViCiT8bK4XGPYy/uSAf0g=',
                    address=('192.168.50.0/24',),
                    listen_port=44100
                ),),
                phone_lines=(WireguardInterface(
                    name='phone_lines0',
                    private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                    public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                    address=(('10.10.200.1/24',)),
                    listen_port=44100,
                ),),
                forums=(WireguardInterface(
                    name='forum0',
                    private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                    public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                    address=(('10.10.10.1/24',)),
                    listen_port=44200,
                ),),
            )
        assert 'has the same listen_port' in str(error.value)

    def test_check_interface_unique4(self):
        """ it raises an error when an interface’s listen port is within the forum range """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(WireguardInterface(
                    public_key='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
                    private_key='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
                    shared_psk='mwn0Dfc4IwYlq/jDL08f9VTCM+mQbV2tJlRdIDAy5CA=',
                    listen_port=44201,
                ),),
                forums=(WireguardInterface(
                    name='forum0',
                    private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                    public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                    address=(('10.10.10.1/24',)),
                    listen_port=44200,
                ),),
                phone_lines=(WireguardInterface(
                    name='phone_lines0',
                    private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                    public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                    address=(('10.10.200.1/24',)),
                    listen_port=44100,
                ),)
            )

        assert 'Make sure the port is in the allowed range and not the same' in str(error.value)

    def test_check_interface_unique5(self):
        """ it raises an error when an interface’s listen port is within the phone line range """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(WireguardInterface(
                    public_key='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
                    private_key='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
                    shared_psk='mwn0Dfc4IwYlq/jDL08f9VTCM+mQbV2tJlRdIDAy5CA=',
                    listen_port=44101
                ),),
                forums=(WireguardInterface(
                    name='forum0',
                    private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                    public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                    address=(('10.10.10.1/24',)),
                    listen_port=44200,
                ),),
                phone_lines=(WireguardInterface(
                    name='phone_lines0',
                    private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                    public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                    address=(('10.10.200.1/24',)),
                    listen_port=44100,
                ),)
            )

        assert 'Make sure the port is in the allowed range and not the same' in str(error.value)

    def test_check_interface_unique6(self):
        """ it raises an error when an forum’s listen port is not within the forums range """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(WireguardInterface(
                    public_key='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
                    private_key='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
                    shared_psk='mwn0Dfc4IwYlq/jDL08f9VTCM+mQbV2tJlRdIDAy5CA=',
                ),),
                forums=(WireguardInterface(
                    name='forum0',
                    private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                    public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                    address=(('10.10.10.1/24',)),
                    listen_port=5000,
                ),),
                phone_lines=(WireguardInterface(
                    name='phone_lines0',
                    private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                    public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                    address=(('10.10.200.1/24',)),
                    listen_port=44100,
                ),)
            )

        assert 'Make sure the port is in the allowed range and not the same' in str(error.value)

    def test_check_interface_unique7(self):
        """ it raises an error when a phone line’s listen port is not within the phone line range """
        with pytest.raises(ValueError) as error:
            HQState(
                federation=Federation(name='a_name'),
                interfaces=(WireguardInterface(
                    public_key='9BMRLFuETS7c2PSgR1UqP3TxFwEaNHaGgGCdF1HoHXI=',
                    private_key='FU2N9kCSHDPOucnBgB0qRECPN0aw+I5H0rHrcyH8F3o=',
                    shared_psk='mwn0Dfc4IwYlq/jDL08f9VTCM+mQbV2tJlRdIDAy5CA=',
                ),),
                forums=(WireguardInterface(
                    name='forum0',
                    private_key='GIITfONf5p+7fX5yGY5U7PWV3Uc+SEfYMGUY9F4/BUc=',
                    public_key='qufw3QuU9lMWBTDLmgWpsk1fQsRTG4UZwyPYgUi9l34=',
                    address=(('10.10.10.1/24',)),
                    listen_port=44200,
                ),),
                phone_lines=(WireguardInterface(
                    name='phone_lines0',
                    private_key='mozYFDybwVjHvy94hWP8Zyff3080xIygsNqDHB0MjkY=',
                    public_key='nLt1mnBG6VyThOASx7b8XFSuldf6R9g4+QYfM1V+8gk=',
                    address=(('10.10.200.1/24',)),
                    listen_port=5000,
                ),)
            )

        assert 'Make sure the port is in the allowed range and not the same' in str(error.value)
