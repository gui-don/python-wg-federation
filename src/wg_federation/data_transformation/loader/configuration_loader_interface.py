from __future__ import annotations

from abc import ABC, abstractmethod


class ConfigurationLoaderInterface(ABC):
    """
    Configuration Loader interface. Represents any configuration loader for a single source.
    """

    @abstractmethod
    def load_from(self, source: str) -> dict:
        """
        Load configuration from the source.
        :param source: source of configuration
        :return: configuration
        """

    @abstractmethod
    def supports(self, source: str) -> bool:
        """
        Whether the configuration loader supports the given source
        :return: True if the configuration loader supports the source, false otherwise.
        """
