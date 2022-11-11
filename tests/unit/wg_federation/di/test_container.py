""" container.py test suit """
import logging
from unittest.mock import patch, MagicMock

from dependency_injector.containers import DeclarativeContainer, DynamicContainer
from wg_federation.di.container import Container


class TestContainer:
    """ Test Container class """

    _logger: logging.Logger = MagicMock()

    _subject: DeclarativeContainer = None

    def setup_method(self):
        """ Constructor """
        self._subject = Container()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, DynamicContainer)

    @patch.dict('os.environ', {'WG_FEDERATION_DEBUG': 'True'})
    def test_early_debug(self):
        """ it sets logger level to DEBUG early when DEBUG env var is set """
        with patch.object(logging, 'getLogger', return_value=self._logger):
            self._subject = Container()

        self._logger.setLevel.assert_called_with(logging.DEBUG)
