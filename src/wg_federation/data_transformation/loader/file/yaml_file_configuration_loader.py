import functools
from pathlib import Path

import yaml
from deepmerge import always_merger

from wg_federation.data_transformation.loader.configuration_loader_interface import ConfigurationLoaderInterface


class YamlFileConfigurationLoader(ConfigurationLoaderInterface):
    """
    Read any configuration from yaml files
    """

    def load_from_all(self, sources: tuple[str]) -> dict:
        return functools.reduce(self.__merge_configuration, sources, {})

    def load_from(self, source: str) -> dict:
        if not Path(source).is_file():
            raise RuntimeError(f'Tried to load configuration from “{source}”. The file does not exist.')

        with open(file=source, mode='r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_supported_source() -> str:
        return 'yaml_file'

    def __merge_configuration(self, previous_configuration: dict, next_source: str) -> dict:
        return always_merger.merge(previous_configuration, self.load_from(next_source))
