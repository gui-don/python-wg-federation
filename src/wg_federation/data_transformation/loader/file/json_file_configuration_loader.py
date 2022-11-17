import json
from io import TextIOWrapper

from wg_federation.data_transformation.loader.file.file_configuration_loader import FileConfigurationLoader
from wg_federation.utils.utils import Utils


class JsonFileConfigurationLoader(FileConfigurationLoader):
    """
    Read any configuration from JSON files
    """

    def supports(self, source: str) -> bool:
        return super().supports(source) and \
            Utils.has_extension(source, 'json')

    @classmethod
    def _load_file(cls, file: TextIOWrapper) -> dict:
        return Utils.always_dict(json.load(file))
