import argparse
import logging
import os
import pathlib
from argparse import ArgumentParser

import portalocker
import xdg
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Hash import Poly1305
from dependency_injector import containers, providers
from nacl import public
from systemd.journal import JournalHandler

from wg_federation.constants import __version__
from wg_federation.controller.baseline.configure_logging_controller import ConfigureLoggingController
from wg_federation.controller.controller_dispatcher import ControllerDispatcher
from wg_federation.crypto.cryptographic_key_deriver import CryptographicKeyDeriver
from wg_federation.crypto.message_encrypter import MessageEncrypter
from wg_federation.crypto.message_signer import MessageSigner
from wg_federation.crypto.wireguard_key_generator import WireguardKeyGenerator
from wg_federation.data_transformation.configuration_location_finder import ConfigurationLocationFinder
from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader
from wg_federation.data_transformation.loader.file.json_file_configuration_loader import JsonFileConfigurationLoader
from wg_federation.data_transformation.loader.file.signature_file_configuration_reader import \
    SignatureFileConfigurationLoader
from wg_federation.data_transformation.loader.file.yaml_file_configuration_loader import YamlFileConfigurationLoader
from wg_federation.data_transformation.loader.proxy.decrypt_configuration_loader_proxy import \
    DecryptConfigurationLoaderProxy
from wg_federation.data_transformation.loader.proxy.verify_signature_configuration_loader_proxy import \
    VerifySignatureConfigurationLoaderProxy
from wg_federation.data_transformation.locker.configuration_locker import ConfigurationLocker
from wg_federation.data_transformation.locker.file_configuration_locker import FileConfigurationLocker
from wg_federation.data_transformation.saver.configuration_saver import ConfigurationSaver
from wg_federation.data_transformation.saver.file.json_file_configuration_saver import JsonFileConfigurationSaver
from wg_federation.data_transformation.saver.file.signature_file_configuration_saver import \
    SignatureFileConfigurationSaver
from wg_federation.data_transformation.saver.file.yaml_file_configuration_saver import YamlFileConfigurationSaver
from wg_federation.data_transformation.saver.proxy.encrypt_configuration_saver_proxy import \
    EncryptConfigurationSaverProxy
from wg_federation.data_transformation.saver.proxy.mutable_transform_configuration_saver_proxy import \
    MutableTransformConfigurationSaverProxy
from wg_federation.data_transformation.saver.proxy.sign_configuration_saver_proxy import SignConfigurationSaverProxy
from wg_federation.input.manager.input_manager import InputManager
from wg_federation.input.reader.argument_reader import ArgumentReader
from wg_federation.input.reader.configuration_file_reader import ConfigurationFileReader
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

        # Crypto
        self.wireguard_key_generator = providers.Singleton(
            WireguardKeyGenerator,
            nacl_public_lib=public,
            cryptodome_random_lib=Random,
        )
        self.cryptographic_key_deriver = providers.Singleton(
            CryptographicKeyDeriver,
            user_input=self.user_input
        )
        self.message_signer = providers.Singleton(
            MessageSigner,
            cryptographic_key_deriver=self.cryptographic_key_deriver,
            cryptodome_poly1305=Poly1305
        )
        self.message_encrypter = providers.Singleton(
            MessageEncrypter,
            cryptographic_key_deriver=self.cryptographic_key_deriver,
            cryptodome_aes=AES
        )

        # data transformation
        self.configuration_location_finder = providers.Singleton(
            ConfigurationLocationFinder,
            user_input=self.user_input,
            xdg_lib=xdg,
            pathlib_lib=pathlib,
            application_name=argparse.ArgumentParser().prog,
        )

        self.configuration_loader = providers.Singleton(
            ConfigurationLoader,
            configuration_loaders=providers.List(
                providers.Singleton(YamlFileConfigurationLoader, pathlib_lib=pathlib),
                providers.Singleton(JsonFileConfigurationLoader, pathlib_lib=pathlib),
                providers.Singleton(SignatureFileConfigurationLoader, pathlib_lib=pathlib),
            ),
            logger=self.root_logger
        )
        self.configuration_locker = providers.Singleton(
            ConfigurationLocker,
            configuration_lockers=providers.List(
                providers.Singleton(
                    FileConfigurationLocker,
                    file_locker=portalocker,
                    path_lib=pathlib,
                ),
            ),
            logger=self.root_logger
        )
        self.verify_signature_configuration_loader_proxy_factory = providers.Factory(
            VerifySignatureConfigurationLoaderProxy,
            configuration_location_finder=self.configuration_location_finder,
            message_signer=self.message_signer
        )
        self.decrypt_configuration_loader_proxy_factory = providers.Factory(
            DecryptConfigurationLoaderProxy,
            message_encrypter=self.message_encrypter
        )

        self.configuration_saver = providers.Singleton(
            ConfigurationSaver,
            configuration_savers=providers.List(
                providers.Singleton(YamlFileConfigurationSaver, pathlib_lib=pathlib),
                providers.Singleton(JsonFileConfigurationSaver, pathlib_lib=pathlib),
                providers.Singleton(SignatureFileConfigurationSaver, pathlib_lib=pathlib, os_lib=os),
            ),
            logger=self.root_logger
        )
        self.mutable_transform_configuration_saver_proxy_factory = providers.Factory(
            MutableTransformConfigurationSaverProxy,
        )
        self.encrypt_configuration_saver_proxy_factory = providers.Factory(
            EncryptConfigurationSaverProxy,
            message_encrypter=self.message_encrypter
        )
        self.sign_configuration_saver_proxy_factory = providers.Factory(
            SignConfigurationSaverProxy,
            configuration_location_finder=self.configuration_location_finder,
            message_signer=self.message_signer,
            digest_configuration_saver=self.configuration_saver,
        )

        # input
        self.environment_variable_reader = providers.Singleton(
            EnvironmentVariableReader,
            logger=self.root_logger
        )
        self.argument_parser = providers.Singleton(ArgumentParser)
        self.configuration_file_reader = providers.Singleton(
            ConfigurationFileReader,
            logger=self.root_logger,
            configuration_loader=self.configuration_loader
        )
        self.argument_reader = providers.Singleton(
            ArgumentReader,
            argument_parser=self.argument_parser,
            program_version=__version__
        )
        self.input_manager = providers.Singleton(
            InputManager,
            argument_reader=self.argument_reader,
            environment_variable_reader=self.environment_variable_reader,
            configuration_file_reader=self.configuration_file_reader,
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
