import json
from typing import TextIO

from wg_federation.data_transformation.loader.file.file_configuration_loader import FileConfigurationLoader


class JsonFileConfigurationLoader(FileConfigurationLoader):
    """
    Read any configuration from JSON files
    """

    @staticmethod
    def get_supported_source() -> str:
        return 'json_file'

    @classmethod
    def _load_file(cls, file: TextIO) -> dict:
        return json.load(file)
