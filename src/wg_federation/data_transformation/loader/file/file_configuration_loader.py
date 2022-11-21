from abc import ABC
from io import TextIOWrapper
from types import ModuleType
from typing import Any

from wg_federation.data_transformation.loader.configuration_loader_interface import ConfigurationLoaderInterface


class FileConfigurationLoader(ConfigurationLoaderInterface, ABC):
    """
    Read any configuration from any kind of files
    """

    _pathlib_lib: ModuleType = None

    def __init__(self, pathlib_lib: ModuleType):
        """
        Constructor
        :param pathlib_lib:
        """
        self._pathlib_lib = pathlib_lib

    def load_from(self, source: Any) -> dict:
        if not isinstance(source, TextIOWrapper):
            with open(file=source, mode='r+', encoding='utf-8') as file:
                return self._load_file(file)

        return self._load_file(source)

    def supports(self, source: Any) -> bool:
        return (isinstance(source, str) and self._pathlib_lib.Path(source).exists()) \
            or isinstance(source, TextIOWrapper)

    def _load_file(self, file: TextIOWrapper) -> dict:
        """
        Process an open file and returns configuration
        :param file: open file handler
        :return: configuration
        """
        file.seek(0)
        return {}
