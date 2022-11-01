from typing import TextIO

import yaml

from wg_federation.data_transformation.loader.file.file_configuration_loader import FileConfigurationLoader


class YamlFileConfigurationLoader(FileConfigurationLoader):
    """
    Read any configuration from YAML files
    """

    @staticmethod
    def get_supported_source() -> str:
        return 'yaml_file'

    @classmethod
    def _load_file(cls, file: TextIO) -> dict:
        return yaml.safe_load(file)
