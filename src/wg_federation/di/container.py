import logging
import os
from argparse import ArgumentParser

from dependency_injector import containers, providers
from systemd.journal import JournalHandler

from wg_federation.constants import __version__
from wg_federation.controller.baseline.configure_logging_controller import ConfigureLoggingController
from wg_federation.controller.controller_dispatcher import ControllerDispatcher
from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader
from wg_federation.data_transformation.loader.file.json_file_configuration_loader import JsonFileConfigurationLoader
from wg_federation.data_transformation.loader.file.yaml_file_configuration_loader import YamlFileConfigurationLoader
from wg_federation.input.manager.input_manager import InputManager
from wg_federation.input.reader.argument_reader import ArgumentReader
from wg_federation.input.reader.environment_variable_reader import EnvironmentVariableReader


# Because it's how the DI lib works
# pylint: disable=too-many-instance-attributes


class Container(containers.DynamicContainer):
    """
    Container class for Dependency Injection
    """

    EARLY_DEBUG: bool = False

    def __init__(self):
        super().__init__()

        early_debug: bool = 'True' == os.getenv(EnvironmentVariableReader.get_real_env_var_name('DEBUG')) or \
                            self.EARLY_DEBUG

        # data input
        self.user_input = providers.Object()

        # logging
        _logger = logging.getLogger('root')
        _logger_console_handler = logging.StreamHandler()
        _logger_syslog_handler = JournalHandler()

        if early_debug:
            # Can help debug very early code, like input processing
            # This is because the controller that sets log level comes after input processing
            _logger.setLevel(logging.DEBUG)
            _logger_console_handler.setLevel(logging.DEBUG)

        _logger.addHandler(_logger_console_handler)
        _logger.addHandler(_logger_syslog_handler)

        self.logger_console_handler = providers.Object(_logger_console_handler)
        self.logger_syslog_handler = providers.Object(_logger_syslog_handler)

        self.root_logger = providers.Object(_logger)

        # input
        self.environment_variable_reader = providers.Singleton(
            EnvironmentVariableReader,
            logger=self.root_logger
        )
        self.argument_parser = providers.Singleton(ArgumentParser)
        self.argument_reader = providers.Singleton(
            ArgumentReader,
            argument_parser=self.argument_parser,
            program_version=__version__
        )
        self.input_manager = providers.Singleton(
            InputManager,
            argument_reader=self.argument_reader,
            environment_variable_reader=self.environment_variable_reader,
            logger=self.root_logger
        )

        # data transformation
        self.configuration_loader = providers.Singleton(
            ConfigurationLoader,
            configuration_loaders=providers.List(
                providers.Singleton(YamlFileConfigurationLoader),
                providers.Singleton(JsonFileConfigurationLoader),
            ),
            logger=self.root_logger
        )

        # controller
        self.controller_dispatcher = providers.Singleton(
            ControllerDispatcher,
            # careful: controller are FIFO. First registered will be the first to run.
            controllers=providers.List(
                providers.Singleton(
                    ConfigureLoggingController, logger_handler=self.logger_console_handler, logger=self.root_logger
                ),
            ),
            logger=self.root_logger
        )
