from pydantic import BaseModel, SecretStr

from wg_federation.data.input.configuration_backend import ConfigurationBackend
from wg_federation.data.input.log_level import LogLevel


class UserInput(BaseModel):
    """
    Data class containing all user inputs
    """
    verbose: bool = None
    debug: bool = None
    quiet: bool = None
    log_level: LogLevel = None
    root_passphrase: SecretStr = None
    state_backend: ConfigurationBackend = None
    state_digest_backend: ConfigurationBackend = None

    arg0: str = None
    arg1: str = None
    arg2: str = None
    arg3: str = None
