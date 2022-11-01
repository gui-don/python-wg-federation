import logging

from wg_federation.data_transformation.loader.configuration_loader_interface import ConfigurationLoaderInterface


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

    def load(self, source_kind: str, sources: tuple[str]):
        """
        Loads different configurations of source_kind from sources
        :param source_kind: kind of sources
        :param sources: sources
        :return: raw configuration
        """
        for _configuration_loader in self._configuration_loaders:
            if source_kind == _configuration_loader.get_supported_source():
                self._logger.debug(
                    f'{_configuration_loader.__class__} configuration loader supports {source_kind}. '
                    f'Trying to load: {"; ".join(sources)}.'
                )

                return _configuration_loader.load_from_all(sources)

        raise RuntimeError(f'Could not load any configuration from “{source_kind}”. '
                           f'It seems no ConfigurationLoader supports this type of source.')
