from dataclasses import dataclass
from typing import cast

from wg_federation.input.data import LogLevel


@dataclass(frozen=True)
class RawOptions:
    """
    Contains metadata for all options, command line arguments, environment variables and options configuration stanzas.
    """

    GENERAL_OPTIONS = {
        'quiet': {
            'argument_short': '-q',
            'argument_alias': '--quiet',
            'type': bool,
            'argparse_action': 'store_true',
            'default': False,
            'description': 'Prevent any messages to appear in the standard output, regardless of other options.'
        },
        'log_level': {
            'argument_short': '-l',
            'argument_alias': '--log-level',
            'type': int,
            'default': 'INFO',
            'description': f'Maximum kind of messages to log. Can be “{"”, “".join([e.name for e in LogLevel])}”.'
        },
        'verbose': {
            'argument_short': '-v',
            'argument_alias': '--verbose',
            'name': 'verbose',
            'type': bool,
            'argparse_action': 'store_true',
            'default': True,
            'description': 'Enabled “verbose” mode. Displays INFO logs in the standard output.'
        },
        'debug': {
            'argument_short': '-vv',
            'argument_alias': '--debug',
            'name': 'debug',
            'type': bool,
            'argparse_action': 'store_true',
            'default': False,
            'description': 'Enabled “debug” mode. Displays DEBUG logs in the standard output.'
        }
    }

    ARGUMENTS = [
        {
            'command': 'help',
            'description': 'Displays help',
        },
        {
            'command': 'hq',
            'description': 'Control the HeadQuarter',
            'subcommands': [
                {
                    'command': 'run',
                    'description': 'Runs the HeadQuarter daemon.',
                },
                {
                    'command': 'bootstrap',
                    'description': 'Bootstrap the HeadQuarter.',
                }
            ],
            'options': [],
        },
    ]

    ALL_OPTIONS = GENERAL_OPTIONS

    @classmethod
    def get_all_options_names(cls) -> list[str]:
        """
        Returns all possible options names
        :return:
        """

        return list(cls.ALL_OPTIONS.keys())

    @classmethod
    def get_argument_depth(cls, _arguments: list[object] = None, _depth_level: int = 1) -> int:
        """
        Returns the maximum number of arguments that may be set
        :param _arguments: List of arguments
        :param _depth_level: Starting depth level
        :return:
        """
        if _arguments is None:
            _arguments = cls.ARGUMENTS

        for arguments in _arguments:
            # Specifically for mypy, since mypy cannot infer argument is a dict in this context
            arguments = cast(dict, arguments)
            if isinstance(arguments.get('subcommands', None), list):
                return cls.get_argument_depth(arguments.get('subcommands'), _depth_level + 1)

        return _depth_level

    @classmethod
    def get_all_argument_keys(cls) -> list[str]:
        """
        Returns all possible argument keys
        :return:
        """

        return list(map(lambda x: 'arg' + str(x), range(cls.get_argument_depth())))
