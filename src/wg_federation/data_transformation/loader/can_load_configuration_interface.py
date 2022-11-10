from abc import ABC, abstractmethod


class CanLoadConfigurationInterface(ABC):
    """
    Interface describing a class that can load any kind of configuration, from a single source or multiple sources.
    """

    @abstractmethod
    def load_if_exists(self, source: str, source_kind: str = '') -> dict:
        """
        Load a configuration source of source_kind, ignoring whether the source can be processed
        :raise InvalidDataError When source was loaded but contains invalid data
        :param source: Source of the configuration
        :param source_kind: Kind of the source of the configuration.
        :return: Configuration as a dict or empty dict if source is unsupported
        """

    @abstractmethod
    def load(self, source: str, source_kind: str = '') -> dict:
        """
        Load a configuration source of source_kind.
        :raise SourceUnsupportedError When source is not supported because no ConfigurationLoader can handle it.
        :raise InvalidDataError When source was loaded but contains invalid data
        :param source: Source of the configuration
        :param source_kind: Force a ConfigurationLoader of the kind to be used. Not recommended but may be useful.
        :return: Configuration as a dict
        """

    @abstractmethod
    def load_all_if_exists(self, sources: tuple[str, ...]) -> dict:
        """
        Load multiple sources and unify them into a single configuration with a deep merge.
        Ignore sources that are not supported
        :raise InvalidDataError When source was loaded but contains invalid data
        :param sources: Sources of the configurations
        :return: Unified configuration as a dict
        """

    @abstractmethod
    def load_all(self, sources: tuple[str, ...]) -> dict:
        """
        Load multiple sources and unify them into a single configuration with a deep merge.
        :raise SourceUnsupportedError When a source is not supported because no ConfigurationLoader can handle it.
        :raise InvalidDataError When source was loaded but contains invalid data
        :param sources: Sources of the configurations
        :return: Unified configuration as a dict
        """
