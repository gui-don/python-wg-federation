import pytest

from wg_federation.data.state.federation import Federation


class TestFederation:
    """ Test Federation class """

    _subject: Federation = None

    def setup_method(self):
        """ Constructor """
        self._subject = Federation(
            name='a_name',
            forum_max_port=5500,
            forum_min_port=5400,
            phone_line_max_port=5600,
            phone_line_min_port=5501,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, Federation)

    def test_data(self):
        """ it returns its data """
        assert 'a_name' == self._subject.name
        assert 5500 == self._subject.forum_max_port
        assert 5400 == self._subject.forum_min_port
        assert 5600 == self._subject.phone_line_max_port
        assert 5501 == self._subject.phone_line_min_port

    def test_port_within_forum_range(self):
        """ it returns whether or not a given port is part of the forum ports range """
        assert self._subject.port_within_forum_range(5400)
        assert self._subject.port_within_forum_range(5450)
        assert not self._subject.port_within_forum_range(5000)

    def test_port_within_phone_line_range(self):
        """ it returns whether or not a given port is part of the phone line ports range """
        assert not self._subject.port_within_phone_line_range(5400)
        assert not self._subject.port_within_phone_line_range(5450)
        assert self._subject.port_within_phone_line_range(5555)

    def test_check_name(self):
        """ it raises an error when the federation name is not valid """
        for wrong_name in [
            'not a valid name',
            '*invalid_federation',
            '',
            'this_is_a_name_too_long-this_is_a_name_too_long-this_is_a_name_too_long-this_is_a_name_too_long-this_is_a_name_too_long',
        ]:
            with pytest.raises(ValueError):
                Federation(name=wrong_name)

    def test_check_forum_port(self):
        """ it raises an error when forum max and min port range is less than 10 """
        with pytest.raises(ValueError) as error:
            Federation(
                name='a_name',
                forum_max_port=5000,
                forum_min_port=5005,
            )
        assert 'be at minimum 10' in str(error.value)

    def test_check_forum_port2(self):
        """ it raises an error when forum max and min port range is more than 100 """
        with pytest.raises(ValueError) as error:
            Federation(
                name='a_name',
                forum_max_port=5500,
                forum_min_port=5000,
            )
        assert 'be at maximum 100' in str(error.value)

    def test_check_forum_port3(self):
        """ it raises an error when forum max and min ports are under 1000 """
        with pytest.raises(ValueError):
            Federation(
                name='a_name',
                forum_max_port=900,
                forum_min_port=880,
            )

    def test_check_forum_port4(self):
        """ it raises an error when forum max port is below min port """
        with pytest.raises(ValueError):
            Federation(
                name='a_name',
                forum_max_port=9000,
                forum_min_port=9050,
            )

    def test_check_phone_line_port(self):
        """ it raises an error when phone line max and min port range is less than 10 """
        with pytest.raises(ValueError) as error:
            Federation(
                name='a_name',
                phone_line_max_port=5000,
                phone_line_min_port=5005,
            )
        assert 'be at minimum 10' in str(error.value)

    def test_check_phone_line_port2(self):
        """ it raises an error when phone line max and min port range is more than 100 """
        with pytest.raises(ValueError) as error:
            Federation(
                name='a_name',
                phone_line_max_port=5500,
                phone_line_min_port=5000,
            )
        assert 'be at maximum 100' in str(error.value)

    def test_check_phone_line_port3(self):
        """ it raises an error when phone line max and min ports are under 1000 """
        with pytest.raises(ValueError):
            Federation(
                name='a_name',
                phone_line_max_port=900,
                phone_line_min_port=880,
            )

    def test_check_phone_line_port4(self):
        """ it raises an error when phone line max port is below min port """
        with pytest.raises(ValueError):
            Federation(
                name='a_name',
                phone_line_max_port=9000,
                phone_line_min_port=9050,
            )

    def test_from_dict(self):
        """ it instantiates itself using a dict of values """
        assert isinstance(Federation.from_dict({
            'name': 'a_name',
            'forum_max_port': 5500,
            'forum_min_port': 5400,
            'phone_line_max_port': 5600,
            'phone_line_min_port': 5501,
        }), Federation)
