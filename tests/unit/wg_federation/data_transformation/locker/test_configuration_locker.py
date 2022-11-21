import pytest
from mockito import mock, when, verifyNoMoreInteractions, expect, verifyNoUnwantedInteractions, unstub
from mockito.mocking import _Dummy

from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader
from wg_federation.data_transformation.locker.can_lock_configuration_interface import CanLockConfigurationInterface
from wg_federation.data_transformation.locker.configuration_locker import ConfigurationLocker
from wg_federation.exception.developer.data_transformation.lock_unsupported_error import LockUnsupportedError


class TestConfigurationLocker:
    """ Test ConfigurationLocker class """

    _working_configuration_locker = mock()
    _working_configuration_locker2 = mock()
    _logger = mock()

    _subject: ConfigurationLocker = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        when(self._working_configuration_locker).is_default_for(...).thenReturn(False)
        when(self._working_configuration_locker).is_default_for('location1').thenReturn(True)
        when(self._working_configuration_locker2).is_default_for(...).thenReturn(False)
        when(self._working_configuration_locker2).is_default_for('location2').thenReturn(True)

        self._subject = ConfigurationLocker(
            configuration_lockers=(
                self._working_configuration_locker,
                self._working_configuration_locker2,
            ),
            logger=self._logger
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ConfigurationLocker)
        assert isinstance(self._subject, CanLockConfigurationInterface)

    def test_lock_exclusively(self):
        """ it tries to obtain an exclusive lock of a location """

        expect(self._working_configuration_locker2, times=1).obtain_exclusive_lock('location2').thenReturn(True)
        expect(self._working_configuration_locker, times=0).obtain_exclusive_lock('location2').thenReturn(None)

        self._subject.lock_exclusively('location2')

        verifyNoUnwantedInteractions()
        verifyNoMoreInteractions()

    def test_lock_exclusively2(self):
        """ it tries to obtain an exclusive lock of a location, given a specific configuration locker """

        expect(self._working_configuration_locker2, times=0).obtain_exclusive_lock('location2').thenReturn(True)
        expect(self._working_configuration_locker, times=1).obtain_exclusive_lock('location2').thenReturn(None)

        self._subject.lock_exclusively('location2', _Dummy)

        verifyNoUnwantedInteractions()
        verifyNoMoreInteractions()

    def test_lock_exclusively3(self):
        """ it raises an error if no ConfigurationLocker can lock exclusively the given location """

        with pytest.raises(LockUnsupportedError) as error:
            self._subject.lock_exclusively('unknown')

        assert 'Failed to lock' in str(error)
        assert 'No default ConfigurationLockInterface class for' in str(error)

    def test_lock_exclusively4(self):
        """ it raises an error if the given ConfigurationLock cannot lock exclusively the given location """

        with pytest.raises(LockUnsupportedError) as error:
            self._subject.lock_exclusively('location2', ConfigurationLoader)

        assert 'Failed to lock' in str(error)
        assert 'does not implement a ConfigurationLockInterface' in str(error)

    def test_lock_shared(self):
        """ it tries to obtain a shared lock of a location """

        expect(self._working_configuration_locker2, times=1).obtain_shared_lock('location2').thenReturn(True)
        expect(self._working_configuration_locker, times=0).obtain_shared_lock('location2').thenReturn(None)

        self._subject.lock_shared('location2')

        verifyNoUnwantedInteractions()
        verifyNoMoreInteractions()

    def test_lock_shared2(self):
        """ it tries to obtain a shared lock of a location, given a specific configuration locker """

        expect(self._working_configuration_locker2, times=0).obtain_shared_lock('location2').thenReturn(True)
        expect(self._working_configuration_locker, times=1).obtain_shared_lock('location2').thenReturn(None)

        self._subject.lock_shared('location2', _Dummy)

        verifyNoUnwantedInteractions()
        verifyNoMoreInteractions()

    def test_lock_shared3(self):
        """ it raises an error if no ConfigurationLocker can lock shared the given location """

        with pytest.raises(LockUnsupportedError) as error:
            self._subject.lock_shared('unknown')

        assert 'Failed to lock' in str(error)
        assert 'No default ConfigurationLockInterface class for' in str(error)

    def test_lock_shared4(self):
        """ it raises an error if the given ConfigurationLock cannot lock shared the given location """

        with pytest.raises(LockUnsupportedError) as error:
            self._subject.lock_shared('location2', ConfigurationLoader)

        assert 'Failed to lock' in str(error)
        assert 'does not implement a ConfigurationLockInterface' in str(error)
