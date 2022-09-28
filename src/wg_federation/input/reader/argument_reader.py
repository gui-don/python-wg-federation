from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter, RawTextHelpFormatter

from wg_federation.input.data.raw_options import RawOptions
from wg_federation.input.reader.environment_variable_reader import EnvironmentVariableReader


class ArgumentReader:
    """
    Read & manipulate command line arguments
    """

    _argument_parser: ArgumentParser
    _program_version: str

    def __init__(
            self,
            argument_parser: ArgumentParser,
            program_version: str,
    ):
        """
        Constructor
        :param argument_parser:
        :param program_version:
        """
        self._argument_parser = argument_parser
        self._program_version = program_version

    def _setup_sub_parser(
            self, _parent_argument_parser: ArgumentParser, _arguments: list, depth: int = 0
    ) -> None:
        subparser_action = _parent_argument_parser.add_subparsers(required=False, dest='arg' + str(depth))

        for argument in _arguments:
            parser = subparser_action.add_parser(
                argument.get('command'),
                help=argument.get('description', ''),
                formatter_class=ArgumentDefaultsHelpFormatter
            )
            self._setup_general_options(parser)
            if len(argument.get('subcommands', [])) != 0:
                self._setup_sub_parser(parser, argument.get('subcommands', []), depth + 1)

    def _setup_general_options(self, _parser: ArgumentParser) -> None:
        """
        Setup command line general options
        :param _parser:
        :return:
        """
        for option in RawOptions.GENERAL_OPTIONS.values():
            _parser.add_argument(
                str(option.get('argument_short')),
                str(option.get('argument_alias')),
                dest=str(option.get('name', '')),
                action=str(option.get('argparse_action', 'store')),
                help=f"{option.get('description', '')} "
                     f"Defaults to “{option.get('default') if option.get('default', None) is not None else ''}”.",
            )
        _parser.add_argument(
            '-V',
            '--version',
            action='version',
            version=self._program_version,
            help='Shows the version number and exit.'
        )

    def parse_all(self) -> Namespace:
        """
        Parse all command line options and arguments
        :return: Command line arguments values
        """

        self._argument_parser.description = f"""
{self._argument_parser.prog} can be configured in three ways. By order of precedence, first is overridden by last:
  1. Configuration file
  2. Environment variables
  3. Command line options

  {self._argument_parser.epilog if self._argument_parser.epilog is not None else ''}

environment variables:
  {(chr(10) + "  ").join(
            f"{EnvironmentVariableReader.get_real_env_var_name(name):30} {option.get('description')}"
            for name, option in RawOptions.ALL_OPTIONS.items()
        )}
"""

        self._argument_parser.formatter_class = RawTextHelpFormatter
        self._setup_general_options(self._argument_parser)

        self._setup_sub_parser(self._argument_parser, RawOptions.ARGUMENTS)

        return self._argument_parser.parse_args()
