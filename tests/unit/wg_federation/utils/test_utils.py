from wg_federation.utils.utils import Utils


class TestUtils:
    """ Test Utils class """

    def test_classname(self):
        """ it returns classnames in a specific formatted way """
        assert 'Utils♦' == Utils.classname(Utils())
        assert 'type♦' == Utils.classname(str)
        assert 'Exception♦' == Utils.classname(Exception())

    def test_always_dict(self):
        """ it a dict from any sources """
        assert {} == Utils.always_dict(Utils())
        assert {} == Utils.always_dict('')
        assert {} == Utils.always_dict(123)
        assert {'one': True} == Utils.always_dict({'one': True})
