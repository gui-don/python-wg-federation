from typing import Type, Any

from pydantic import BaseModel


class CommandLineOption(BaseModel):
    """ Data class representing a command line option """

    argparse_action: str = 'store'
    argument_alias: str = None
    argument_short: str = None
    default: Any = None
    description: str = None
    name: str
    type: Type = None
