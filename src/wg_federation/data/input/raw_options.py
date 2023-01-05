from collections.abc import Sequence

from wg_federation.data.input.command_line.argparse_action import ArgparseAction
from wg_federation.data.input.command_line.command_line_argument import CommandLineArgument
from wg_federation.data.input.command_line.command_line_option import CommandLineOption
from wg_federation.data.input.user_input import UserInput
from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.wireguard_interface import WireguardInterface
from wg_federation.utils.utils import Utils


class RawOptions:
    """
    Contains metadata for all options, command line arguments, environment variables and options configuration stanzas.
    """

    options: list[str, CommandLineOption] = list(  # type: ignore
        (CommandLineOption.from_dict(option_name, option) for option_name, option in  # type: ignore
         Utils.extract_attributes(UserInput, ('category', 'general')).items())
    )

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
                    options=list(
                        CommandLineOption.from_dict(option_name, option) for option_name, option in  # type: ignore
                        Utils.extract_attributes(UserInput, ('category', 'bootstrap')).items()
                    )
                ),
                CommandLineArgument(
                    command='get-private-key',
                    description='Fetch the private key of a given interface.',
                    options=[
                        CommandLineOption(
                            argparse_action=ArgparseAction.STORE,
                            argument_alias='--interface-type',
                            argument_short='-t',
                            default=None,
                            description='The type of interface to retrieve the private key from. '
                            # pylint: disable=line-too-long
                                        f'Choices: “{"”, “".join(Utils.extract_attributes(HQState, ("true_type", tuple[WireguardInterface, ...])).keys())}”.',
                            name='interface_type',
                        ),
                        CommandLineOption(
                            argparse_action=ArgparseAction.STORE,
                            argument_alias='--interface-name',
                            argument_short='-i',
                            default=None,
                            description='The name of the interface to retrieve the private key from.',
                            name='interface_name',
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
        return list(map(lambda x: x.name, cls.options))

    @classmethod
    def get_argument_depth(cls, _arguments: list[CommandLineArgument] = None, _depth_level: int = None) -> int:
        """
        Returns the maximum number of arguments that may be set
        :param _arguments: List of arguments
        :param _depth_level: Starting depth level
        :return:
        """
        if not _depth_level:
            _depth_level = 0

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
