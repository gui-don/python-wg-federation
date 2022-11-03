import os
from abc import ABC
from typing import TextIO

from wg_federation.data_transformation.loader.configuration_loader_interface import ConfigurationLoaderInterface


class FileConfigurationLoader(ConfigurationLoaderInterface, ABC):
    """
    Read any configuration from any kind of files
    """

    def load_from(self, source: str) -> dict:
        with open(file=source, mode='r', encoding='utf-8') as file:
            return self._load_file(file)

    @classmethod
    def _load_file(cls, file: TextIO) -> dict:
        """
        Process an open file and returns configuration
        :param file: open file handler
        :return: configuration
        """

    def supports(self, source: str) -> bool:
        return os.path.isfile(source)
