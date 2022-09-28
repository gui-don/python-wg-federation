""" container.py test suit """
from dependency_injector.containers import DynamicContainer

from wg_federation.di.container import Container


class TestContainer:
    """ Test Container class """

    _subject: Container = None

    def setup(self):
        """ Constructor """
        self._subject = Container()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, DynamicContainer)
