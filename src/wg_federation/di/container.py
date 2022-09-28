import logging

from argparse import ArgumentParser
from dependency_injector import containers, providers
from wg_federation.input.reader.environment_variable_reader import EnvironmentVariableReader
from wg_federation.input.reader.argument_reader import ArgumentReader
from wg_federation.input.manager.input_manager import InputManager
from wg_federation.constants import __version__


class Container(containers.DeclarativeContainer):
    """
    Container class for Dependency Injection
    """

    # data
    user_input = providers.Object()

    # logging
    logger = logging.getLogger('root')
    # This is temporary
    # To remove once a controller can do the same thing depending on user inputs
    logging.basicConfig(level=logging.DEBUG)
    root_logger = providers.Object(logger)

    # input
    environment_variable_reader = providers.Singleton(
        EnvironmentVariableReader,
        logger=root_logger
    )
    argument_parser = providers.Singleton(ArgumentParser)
    argument_reader = providers.Singleton(
        ArgumentReader,
        argument_parser=argument_parser,
        program_version=__version__
    )
    input_manager = providers.Singleton(
        InputManager,
        argument_reader=argument_reader,
        environment_variable_reader=environment_variable_reader,
        logger=root_logger
    )
