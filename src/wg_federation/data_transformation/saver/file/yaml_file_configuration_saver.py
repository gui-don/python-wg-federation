from io import TextIOWrapper
from typing import Any

import yaml

from wg_federation.data_transformation.saver.file.file_configuration_saver import FileConfigurationSaver
from wg_federation.utils.utils import Utils


class YamlFileConfigurationSaver(FileConfigurationSaver):
    """
    Save any configuration to JSON files
    """

    def supports(self, data: dict, destination: Any) -> bool:
        return super().supports(data, destination) and \
            Utils.has_extension(super()._get_destination_name(destination), '(yaml|yml)')

    @classmethod
    def _save_data(cls, data: dict, file: TextIOWrapper) -> None:
        super()._save_data(data, file)
        yaml.safe_dump(data, file)