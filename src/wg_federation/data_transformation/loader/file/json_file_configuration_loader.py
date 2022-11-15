import json
import re
from pathlib import Path
from typing import TextIO

from wg_federation.data_transformation.loader.file.file_configuration_loader import FileConfigurationLoader
from wg_federation.utils.utils import Utils


class JsonFileConfigurationLoader(FileConfigurationLoader):
    """
    Read any configuration from JSON files
    """

    def supports(self, source: str) -> bool:
        return super().supports(source) and \
            bool(re.match(r'^\.json$', Path(source).suffix, re.IGNORECASE))

    @classmethod
    def _load_file(cls, file: TextIO) -> dict:
        return Utils.always_dict(json.load(file))
