import functools
import logging

from deepmerge import always_merger

from wg_federation.data_transformation.loader.configuration_loader_interface import ConfigurationLoaderInterface
from wg_federation.exception.developer.data_transformation.source_cannot_be_processed_error import \
    SourceCannotBeProcessedError


class ConfigurationLoader:
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
        """
        Load a configuration source of source_kind, ignoring if the source can be processed
        :param source: Source of the configuration
        :param source_kind: Kind of the source of the configuration
        :return: Configuration as a dict or empty dict if source cannot be processed
        """
        try:
            return self.load(source, source_kind)
        except SourceCannotBeProcessedError:
            return {}

    def load(self, source: str, source_kind: str = '') -> dict:
        """
        Load a configuration source of source_kind.
        :raise SourceCannotBeProcessedError when source cannot be processes
        :param source: Source of the configuration
        :param source_kind: Force a ConfigurationLoader of the kind to be used. Not recommended but may be useful.
        :return: Configuration as a dict
        """
        for _configuration_loader in self._configuration_loaders:
            if _configuration_loader.supports(source) or source_kind == _configuration_loader.get_supported_source():
                self._logger.debug(f'{_configuration_loader.__class__} configuration loader supports {source}.')

                return _configuration_loader.load_from(source)

        raise SourceCannotBeProcessedError(f'Could not load any configuration from “{source} ({source_kind})”. '
                                           f'It seems no ConfigurationLoader supports this type of source.')

    def load_all_if_exists(self, sources: tuple[str, ...]) -> dict:
        """
        Load multiple sources and unify them into a single configuration with a deep merge.
        Ignore sources that cannot be processed
        :param sources: Sources of the configurations
        :return: Unified configuration as a dict
        """
        return functools.reduce(self.__merge_configuration_if_exists, sources, {})

    def load_all(self, sources: tuple[str, ...]) -> dict:
        """
        Load multiple sources and unify them into a single configuration with a deep merge.
        :param sources: Sources of the configurations
        :return: Unified configuration as a dict
        """
        return functools.reduce(self.__merge_configuration, sources, {})

    def __merge_configuration(self, previous_configuration: dict, next_source: str) -> dict:
        return always_merger.merge(previous_configuration, self.load(next_source))

    def __merge_configuration_if_exists(self, previous_configuration: dict, next_source: str) -> dict:
        return always_merger.merge(previous_configuration, self.load_if_exists(next_source))
