from abc import ABC, abstractmethod
from typing import Generator


class CanLockConfigurationInterface(ABC):
    """
    Interface describing a class that can lock any kind of configuration.
    """

    @abstractmethod
    def lock_exclusive(self, location: str, configuration_locker: type = None) -> Generator:
        """
        Lock a location, with an exclusive lick.
        :param location: Location to be locked.
        :param configuration_locker: ConfigurationLock class to use
        :raise LockUnsupportedError if the location have no default or lock_class is not a ConfigurationLockerInterface
        :return: a handle of the locked location
        """

    @abstractmethod
    def lock_shared(self, location: str, configuration_locker: type = None) -> Generator:
        """
        Lock a location, with a shared lock
        :param location: Location to be locked.
        :param configuration_locker: ConfigurationLock class to use
        :raise LockUnsupportedError if the location have no default or lock_class is not a ConfigurationLockerInterface
        :return: a handle of the locked location
        """
