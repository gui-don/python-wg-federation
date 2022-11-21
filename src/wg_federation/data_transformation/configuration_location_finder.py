from types import ModuleType
from typing import Any

from wg_federation.data.input.configuration_backend import ConfigurationBackend
from wg_federation.data.input.user_input import UserInput
from wg_federation.exception.user.data_transformation.configuration_backend_unsupported import \
    ConfigurationBackendUnsupported


class ConfigurationLocationFinder:
    """
    Determines sources of configuration based on use options.
    """
    _user_input: UserInput = None
    _xdg_lib: ModuleType = None
    _pathlib_lib: ModuleType = None
    _application_name: str = None

    def __init__(self, user_input: UserInput, xdg_lib: ModuleType, pathlib_lib: ModuleType, application_name: str):
        self._user_input = user_input
        self._xdg_lib = xdg_lib
        self._pathlib_lib = pathlib_lib
        self._application_name = application_name

    def state_digest(self) -> Any:
        """
        Return the state digest source/destination, according to current context/user inputs.
        :return:
        """
        if ConfigurationBackend.FILE == self._user_input.state_digest_backend:
            return str(self._pathlib_lib.Path(
                self._xdg_lib.xdg_data_home(),
                self._application_name,
                'state.digest'
            ))

        return self.state()

    def state(self) -> Any:
        """
        Return the state source/destination, according to current context/user inputs.
        :return:
        """
        if ConfigurationBackend.FILE == self._user_input.state_backend:
            return str(self._pathlib_lib.Path(
                self._xdg_lib.xdg_data_home(),
                self._application_name,
                'state.json'
            ))

        raise ConfigurationBackendUnsupported(f'“{self._user_input.state_backend}” is not supported for the state.')

    def state_digest_belongs_to_state(self) -> bool:
        """
        Whether the state digest should be part of the state
        :return: True if the state digest should be within the state, False otherwise
        """
        return ConfigurationBackend.DEFAULT == self._user_input.state_digest_backend
