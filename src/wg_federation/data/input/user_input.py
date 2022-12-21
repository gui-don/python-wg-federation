from pydantic import BaseModel, validator, SecretStr

from wg_federation.data.input.command_line.secret_retreival_method import SecretRetrievalMethod
from wg_federation.data.input.configuration_backend import ConfigurationBackend
from wg_federation.data.input.log_level import LogLevel
from wg_federation.exception.developer.data.data_validation_error import DataValidationError


class UserInput(BaseModel):
    """
    Data class containing all user inputs
    """
    # general
    verbose: bool = None
    debug: bool = None
    quiet: bool = None
    log_level: LogLevel = None
    root_passphrase: SecretStr = None
    state_backend: ConfigurationBackend = None
    state_digest_backend: ConfigurationBackend = None
    root_passphrase_command: str = None

    # arguments
    arg0: str = None
    arg1: str = None
    arg2: str = None
    arg3: str = None

    # hq bootstrap
    private_key_retrieval_method: SecretRetrievalMethod = None

    # pylint: disable=no-self-argument
    @validator('private_key_retrieval_method')
    def check_private_key_retrieval_method(cls, value: SecretRetrievalMethod, values: dict) -> SecretRetrievalMethod:
        """
        Validate private_key_retrieval_method
        :param value: passphrase_retrieval_method value
        :param values: rest of the current object’s attributes
        :return:
        """
        if value == SecretRetrievalMethod.WG_FEDERATION_COMMAND and not values.get('root_passphrase_command'):
            raise DataValidationError(
                f'The method to retrieve WireGuard interface’s private keys was set to '
                f'“{SecretRetrievalMethod.WG_FEDERATION_COMMAND.value}” '
                f'(the default value for this setting), '
                f'but you did not provide a command to get the root passphrase dynamically. '
                f'Please set --root-passphrase-command or choose another method.'
            )

        return value
