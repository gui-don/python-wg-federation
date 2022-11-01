from abc import ABC, abstractmethod


class ConfigurationLoaderInterface(ABC):
    """
    Configuration Loader interface. Represents any configuration loader
    """

    @abstractmethod
    def load_from_all(self, sources: tuple[str]) -> dict:
        """
        Look at all given sources and return an unified configuration.
        :param sources: Source. Order is important. Last source will have precedence for the merge of configurations
        :return: configuration
        """

    @abstractmethod
    def load_from(self, source: str) -> dict:
        """
        Load configuration from the source.
        :param source: source of configuration
        :return: configuration
        """

    @staticmethod
    @abstractmethod
    def get_supported_source() -> str:
        """
        Whether the configuration loader supports the given source
        :return: The kind of source this configuration loader supports.
        """
