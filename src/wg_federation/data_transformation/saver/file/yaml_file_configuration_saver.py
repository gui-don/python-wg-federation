from typing import TextIO, Any

import yaml

from wg_federation.data_transformation.saver.file.file_configuration_saver import FileConfigurationSaver
from wg_federation.utils.utils import Utils


class YamlFileConfigurationSaver(FileConfigurationSaver):
    """
    Save any configuration to JSON files
    """

    def supports(self, data: dict, destination: Any) -> bool:
        return super().supports(data, destination) and \
            (isinstance(destination, TextIO) or Utils.has_extension(destination, 'yaml'))

    @classmethod
    def _save_data(cls, data: dict, file: TextIO) -> None:
        yaml.safe_dump(data, file)
