from typing import Type, Any

from pydantic import BaseModel

from wg_federation.input.data.argparse_action import ArgparseAction


class CommandLineOption(BaseModel):
    """ Data class representing a command line option """

    argparse_action: ArgparseAction = ArgparseAction.STORE
    argument_alias: str = None
    argument_short: str = None
    default: Any = None
    description: str = None
    name: str
    type: Type = None
