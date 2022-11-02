import argparse
import logging
import os

import xdg

from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader


class ConfigurationFileReader:
    """
    Read & manipulate configuration files in the current system.
    This class is UNIX-specific.
    """

    _logger: logging.Logger = None
    _configuration_loader: ConfigurationLoader = None

    def __init__(self, logger: logging.Logger, configuration_loader: ConfigurationLoader):
        """
        Constructor
        :param logger:
        :param configuration_loader:
        """
        self._logger = logger
        self._configuration_loader = configuration_loader

    def load_all(self) -> dict:
        """
        Loads all configuration files into a unified dictionary.
        :return:
        """
        sources = (
            f'/etc/{argparse.ArgumentParser().prog}/main.yaml',
            f'{xdg.xdg_data_home()}/{argparse.ArgumentParser().prog}/main.yaml',
        )

        self._logger.debug(
            f'Trying to load configuration files:{os.linesep}  - '
            f'{(os.linesep + "  - ").join(sources)}'
        )

        return self._configuration_loader.load_all_if_exists((
            f'/etc/{argparse.ArgumentParser().prog}/main.yaml',
            f'{xdg.xdg_data_home()}/{argparse.ArgumentParser().prog}/main.yaml',
        ))
