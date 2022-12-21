from collections.abc import Sequence
from typing import Union

from pydantic import SecretStr

from wg_federation.data.input.command_line.argparse_action import ArgparseAction
from wg_federation.data.input.command_line.command_line_argument import CommandLineArgument
from wg_federation.data.input.command_line.command_line_option import CommandLineOption
from wg_federation.data.input.command_line.secret_retreival_method import SecretRetrievalMethod
from wg_federation.data.input.configuration_backend import ConfigurationBackend
from wg_federation.data.input.log_level import LogLevel


class RawOptions:
    """
    Contains metadata for all options, command line arguments, environment variables and options configuration stanzas.
    """

    options: dict[str, CommandLineOption] = {
        'quiet': CommandLineOption(
            argparse_action=ArgparseAction.STORE_TRUE,
            argument_alias='--quiet',
            argument_short='-q',
            default=False,
            description='Prevent any messages to appear in the standard output, regardless of other options.',
            name='quiet',
            type=bool,
        ),

        'log_level': CommandLineOption(
            argparse_action=ArgparseAction.STORE,
            argument_alias='--log-level',
            argument_short='-l',
            default=LogLevel.INFO.value,
            description=f'Maximum kind of messages to log. Can be “{"”, “".join([e.value for e in LogLevel])}”.',
            name='log_level',
            type=str,
        ),

        'verbose': CommandLineOption(
            argparse_action=ArgparseAction.STORE_TRUE,
            argument_alias='--verbose',
            argument_short='-v',
            default=False,
            description='Enabled “verbose” mode. Displays INFO logs in the standard output.',
            name='verbose',
            type=bool,
        ),

        'debug': CommandLineOption(
            argparse_action=ArgparseAction.STORE_TRUE,
            argument_alias='--debug',
            argument_short='-vv',
            default=False,
            description='Enabled “debug” mode. Displays DEBUG logs in the standard output.',
            name='debug',
            type=bool,
        ),

        'root_passphrase': CommandLineOption(
            argparse_action=ArgparseAction.STORE,
            argument_alias='--root-passphrase',
            argument_short='-P',
            default=None,
            description='Root passphrase used to encrypt and decrypt all secrets managed by this program.',
            name='root_passphrase',
            type=SecretStr,
        ),

        'root_passphrase_command': CommandLineOption(
            argparse_action=ArgparseAction.STORE,
            argument_alias='--root-passphrase-command',
            argument_short='--Pcmd',
            default=None,
            description='Process command to call to get the root passphrase. '
                        'If the root passphrase is retrieved through any other means, this will be ignored. '
                        'CAREFUL: this command is unprotected. It MUST NOT contain any secrets.',
            name='root_passphrase_command',
            type=str,
        ),

        'state_backend': CommandLineOption(
            argparse_action=ArgparseAction.STORE,
            argument_alias='--state-backend',
            argument_short='--sb',
            default=ConfigurationBackend.FILE.value,
            description=f'What backend to use for the state. '
                        f'Can be “{"”, “".join([e.value for e in ConfigurationBackend])}”.',
            name='state_backend',
            type=str,
        ),

        'state_digest_backend': CommandLineOption(
            argparse_action=ArgparseAction.STORE,
            argument_alias='--state-digest-backend',
            argument_short='--sdb',
            default=ConfigurationBackend.FILE.value,
            description=f'What backend to use for the digest state. '
                        f'If “DEFAULT” is used, digest will be merged with state_backend.'
                        f'Can be “{"”, “".join([e.value for e in ConfigurationBackend])}”.',
            name='state_digest_backend',
            type=str,
        ),
    }

    arguments: list[CommandLineArgument] = [
        CommandLineArgument(
            command='hq',
            description='HQ commands',
            subcommands=[
                CommandLineArgument(
                    command='run',
                    description='Runs the HeadQuarter daemon.',
                ),
                CommandLineArgument(
                    command='bootstrap',
                    description='Bootstrap the HeadQuarter.',
                    options=[
                        CommandLineOption(
                            argparse_action=ArgparseAction.STORE,
                            argument_alias='--private-key-retrieval-method',
                            argument_short='--PKrm',
                            default=SecretRetrievalMethod.WG_FEDERATION_COMMAND.value,
                            description='What method to use to retrieve the WireGuard private keys for wg-quick. '
                                        f'Possible values: “{"”, “".join([e.value for e in SecretRetrievalMethod])}”. '
                                        f'“{SecretRetrievalMethod.WG_FEDERATION_COMMAND.value}” expects '
                                        f'--root-passphrase-command to be set.'
                                        f'“{SecretRetrievalMethod.TEST_INSECURE_CLEARTEXT.value}” is discouraged.',
                            name='private_key_retrieval_method',
                            type=str,
                        ),
                    ],
                ),
                CommandLineArgument(
                    command='add-interface',
                    description='Add a wireguard interface to the Federation.',
                ),
                CommandLineArgument(
                    command='remove-interface',
                    description='Remove a wireguard interface to the Federation.',
                ),
            ],
        )
    ]

    @classmethod
    def get_all_argument_options_names(
            cls, arguments: list[CommandLineArgument], options: list[str] = None
    ) -> list[str]:
        """
        Gets all option names for a given list of CommandLineArgument.
        :param arguments:
        :param options: Used internally for recursive function, ignore this.
        :return:
        """
        if options is None:
            options = []

        for argument in arguments:
            for option in argument.options:
                options.append(option.name)
            if argument.subcommands:
                cls.get_all_argument_options_names(argument.subcommands, options)

        return options

    @classmethod
    def get_all_options_names(cls) -> list[str]:
        """
        Returns all possible options names
        :return:
        """
        return list(cls.options.keys())

    @classmethod
    def get_argument_depth(cls, _arguments: list[CommandLineArgument] = None, _depth_level: int = 0) -> int:
        """
        Returns the maximum number of arguments that may be set
        :param _arguments: List of arguments
        :param _depth_level: Starting depth level
        :return:
        """
        if _arguments is None:
            _arguments = cls.arguments

        for arguments in _arguments:
            if isinstance(arguments.subcommands, Sequence):
                return cls.get_argument_depth(arguments.subcommands, _depth_level + 1)

        return _depth_level

    @classmethod
    def get_all_argument_keys(cls) -> list[str]:
        """
        Returns all possible argument keys
        :return:
        """

        return list(map(lambda x: 'arg' + str(x), range(cls.get_argument_depth())))

    @classmethod
    def option_has_default(cls, option_name: str, given_value: Union[bool, str, int]) -> bool:
        """
        Whether given option_name has given_value as a default value
        :param option_name: the option name to check
        :param given_value: the default value
        :return: True if given_value is the default value for option_name, False otherwise
        """

        return given_value == cls.options.get(option_name).default
