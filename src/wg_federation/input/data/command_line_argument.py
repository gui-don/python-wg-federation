from pydantic import BaseModel

from wg_federation.input.data.command_line_option import CommandLineOption


class CommandLineArgument(BaseModel):
    """ Data class representing a command line argument """
    command: str = 'store'
    description: str = None
    subcommands: list['CommandLineArgument'] = None
    options: list[CommandLineOption] = None
