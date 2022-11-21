from io import TextIOWrapper

from mockito import mock

from wg_federation.utils.utils import Utils


class TestUtils:
    """ Test Utils class """

    def test_classname(self):
        """ it returns classnames in a specific formatted way """
        assert 'Utils♦' == Utils.classname(Utils())
        assert 'type♦' == Utils.classname(str)
        assert 'Exception♦' == Utils.classname(Exception())

    def test_always_dict(self):
        """ it returns a dict from any sources """
        assert {} == Utils.always_dict(Utils())
        assert {} == Utils.always_dict('')
        assert {} == Utils.always_dict(123)
        assert {'one': True} == Utils.always_dict({'one': True})

    def test_has_extension(self):
        """ it tests whether a path have a given extension """
        assert Utils.has_extension('/ok.json', 'json')
        assert Utils.has_extension('/ok.JSON', 'json')
        assert Utils.has_extension('../../test.Json', 'json')
        assert Utils.has_extension('test.rtf', '(txt|text|rtf)')
        assert Utils.has_extension('/home/test/test.TXT', '(txt|text|rtf)')
        assert not Utils.has_extension('/home/test/test.yml', '(txt|text|rtf)')
        assert not Utils.has_extension('/home/test/test.doc', 'docx')
        assert not Utils.has_extension('/home/test/yaml', 'yaml')

    def test_has_extension2(self):
        """ it tests whether a file handler have a given extension """
        _file = mock({'name': '/var/test.json'}, spec=TextIOWrapper)

        assert Utils.has_extension(_file, 'json')
        assert not Utils.has_extension(_file, 'yaml')
