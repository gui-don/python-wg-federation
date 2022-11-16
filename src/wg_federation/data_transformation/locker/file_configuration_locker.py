from __future__ import annotations

from contextlib import contextmanager, _GeneratorContextManager
from types import ModuleType

import portalocker

from wg_federation.data_transformation.locker.configuration_locker_interface import ConfigurationLockerInterface


class FileConfigurationLocker(ConfigurationLockerInterface):
    """
    Locks a file
    """

    _file_locker: ModuleType = None
    _os_lib: ModuleType = None

    def __init__(self, file_locker: ModuleType, os_lib: ModuleType) -> None:
        self._file_locker = file_locker
        self._os_lib = os_lib

    def obtain_lock_exclusive(self, location: str) -> _GeneratorContextManager:
        return self._do_lock(
            location,
            'w+',
            self._file_locker.LockFlags.NON_BLOCKING | self._file_locker.LockFlags.EXCLUSIVE
        )

    def obtain_lock_shared(self, location: str) -> _GeneratorContextManager:
        return self._do_lock(
            location,
            'r+',
            self._file_locker.LockFlags.NON_BLOCKING | self._file_locker.LockFlags.SHARED
        )

    def is_default_for(self, location: str) -> bool:
        return self._os_lib.path.isfile(location)

    @contextmanager
    def _do_lock(self, location: str, mode: str, flags: portalocker.LockFlags):
        with self._file_locker.Lock(
                location,
                mode,
                timeout=5,
                flags=flags
        ) as file:
            yield file
