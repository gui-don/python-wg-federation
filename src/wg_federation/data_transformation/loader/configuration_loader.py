import functools
import logging

from deepmerge import always_merger

from wg_federation.data_transformation.loader.can_load_configuration_interface import CanLoadConfigurationInterface
from wg_federation.data_transformation.loader.configuration_loader_interface import ConfigurationLoaderInterface
from wg_federation.exception.developer.data_transformation.source_unsupported_error import SourceUnsupportedError
from wg_federation.utils.utils import Utils


class ConfigurationLoader(CanLoadConfigurationInterface):
    """
    Read any configuration from any sources
    """
    _configuration_loaders: tuple[ConfigurationLoaderInterface, ...] = None
    _logger: logging.Logger = None

    def __init__(
            self,
            configuration_loaders: tuple[ConfigurationLoaderInterface, ...],
            logger: logging.Logger,
    ):
        """
        Constructor
        :param configuration_loaders:
        :param logger:
        """
        self._configuration_loaders = tuple(configuration_loaders)
        self._logger = logger

    def load_if_exists(self, source: str, source_kind: str = '') -> dict:
        try:
            return self.load(source, source_kind)
        except SourceUnsupportedError:
            return {}

    def load(self, source: str, source_kind: str = '') -> dict:
        for _configuration_loader in self._configuration_loaders:
            if _configuration_loader.supports(source) or source_kind == _configuration_loader.get_supported_source():
                self._logger.debug(f'{Utils.classname(_configuration_loader)} '
                                   f'configuration loader supports {source}.')
                return dict(_configuration_loader.load_from(source))

        raise SourceUnsupportedError(f'Could not load any configuration from “{source} ({source_kind})”. '
                                     f'It seems no ConfigurationLoader supports this type of source.')

    def load_all_if_exists(self, sources: tuple[str, ...]) -> dict:
        return functools.reduce(self.__merge_configuration_if_exists, sources, {})

    def load_all(self, sources: tuple[str, ...]) -> dict:
        return functools.reduce(self.__merge_configuration, sources, {})

    def __merge_configuration(self, previous_configuration: dict, next_source: str) -> dict:
        return dict(always_merger.merge(previous_configuration, self.load(next_source)))

    def __merge_configuration_if_exists(self, previous_configuration: dict, next_source: str) -> dict:
        return dict(always_merger.merge(previous_configuration, self.load_if_exists(next_source)))
