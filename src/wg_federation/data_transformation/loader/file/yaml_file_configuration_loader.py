import re
from pathlib import Path
from typing import TextIO

import yaml

from wg_federation.data_transformation.loader.file.file_configuration_loader import FileConfigurationLoader
from wg_federation.utils.utils import Utils


class YamlFileConfigurationLoader(FileConfigurationLoader):
    """
    Read any configuration from YAML files
    """

    @staticmethod
    def get_supported_source() -> str:
        return 'yaml_file'

    def supports(self, source: str) -> bool:
        return super().supports(source) and \
            bool(re.match(r'^\.(yaml|yml)$', Path(source).suffix, re.IGNORECASE))

    @classmethod
    def _load_file(cls, file: TextIO) -> dict:
        return Utils.always_dict(yaml.safe_load(file))
