from enum import Enum
from io import TextIOWrapper

from mockito import mock

from wg_federation.utils.utils import Utils


class StrTestEnum(str, Enum):
    """ Test StrEnum """
    TEST1 = 'test1'
    TEST2 = 'test2'


class IntTestEnum(int, Enum):
    """ Test IntEnum """
    TEST1 = 1
    TEST2 = 2


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

    def test_recursive_map(self):
        """ it performs a function on each element of a multidimentional iterable """

        assert ['content1', 'other1'] == Utils.recursive_map(
            lambda x: str(x) + '1',
            ['content', 'other']
        )

        def test(value):
            if isinstance(value, str):
                return str(value) + '2'
            return value

        assert {'content': {'ok': 'value2'}, '2': ['second2']} == Utils.recursive_map(
            test,
            {'content': {'ok': 'value'}, '2': ['second']}
        )

    def test_enums_to_iterable(self):
        """ it transforms a list of Enums to an iterable list of strings """

        assert ['test1', 'test2'] == Utils.enums_to_iterable([StrTestEnum.TEST1, StrTestEnum.TEST2])
        assert [1, 2] == Utils.enums_to_iterable([IntTestEnum.TEST1, IntTestEnum.TEST2])
