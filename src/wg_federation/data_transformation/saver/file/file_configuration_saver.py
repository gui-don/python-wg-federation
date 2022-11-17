import os.path
from abc import ABC
from io import TextIOWrapper
from typing import Any

from wg_federation.data_transformation.saver.configuration_saver_interface import ConfigurationSaverInterface


class FileConfigurationSaver(ConfigurationSaverInterface, ABC):
    """
    Save any configuration from to kind of files
    """

    def save_to(self, data: dict, destination: Any) -> None:
        if not isinstance(destination, TextIOWrapper):
            with open(file=destination, mode='w', encoding='utf-8') as file:
                self._save_data(data, file)
                return

        self._save_data(data, destination)

    def supports(self, data: dict, destination: Any) -> bool:
        return (isinstance(destination, str) and os.path.isfile(destination)) or isinstance(destination, TextIOWrapper)

    # pylint: disable=unused-argument
    @classmethod
    def _save_data(cls, data: dict, file: TextIOWrapper) -> None:
        """
        Process an open file and returns configuration
        :param file: open file handler
        :return: configuration
        """
        file.truncate(0)

    def _get_destination_name(self, destination: Any):
        if isinstance(destination, TextIOWrapper):
            return destination.name

        return destination
