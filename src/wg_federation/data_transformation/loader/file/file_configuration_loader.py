import functools
from abc import ABC
from pathlib import Path
from typing import TextIO

from deepmerge import always_merger

from wg_federation.data_transformation.loader.configuration_loader_interface import ConfigurationLoaderInterface


class FileConfigurationLoader(ConfigurationLoaderInterface, ABC):
    """
    Read any configuration from any kind of files
    """

    def load_from_all(self, sources: tuple[str]) -> dict:
        return functools.reduce(self.__merge_configuration, sources, {})

    def load_from(self, source: str) -> dict:
        if not Path(source).is_file():
            raise RuntimeError(f'Tried to load configuration from “{source}”. The file does not exist.')

        with open(file=source, mode='r', encoding='utf-8') as file:
            return self._load_file(file)

    @classmethod
    def _load_file(cls, file: TextIO) -> dict:
        """
        Process an open file and returns configuration
        :param file: open file handler
        :return: configuration
        """

    def __merge_configuration(self, previous_configuration: dict, next_source: str) -> dict:
        return always_merger.merge(previous_configuration, self.load_from(next_source))
