import pytest
from mockito import mock, unstub, when, expect, verifyNoUnwantedInteractions, verifyNoMoreInteractions
from portalocker import LockFlags

from wg_federation.data_transformation.locker.configuration_locker_interface import ConfigurationLockerInterface
from wg_federation.data_transformation.locker.file_configuration_locker import FileConfigurationLocker


class TestFileConfigurationLocker:
    """ Test FileConfigurationLocker class """

    _file = None
    _path_mock = None
    _lock = None

    _file_locker = None
    _os_lib = None

    _subject: FileConfigurationLocker = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._file = mock()
        self._lock = mock()
        self._path_mock = mock()

        # pylint: disable=unnecessary-dunder-call
        when(self._lock).__enter__(...).thenReturn(self._file)
        when(self._lock).__exit__(...).thenReturn(self._file)

        self._file_locker = mock({'LockFlags': LockFlags})
        self._os_lib = mock({'path': self._path_mock})

        when(self._file_locker).Lock(...).thenReturn(self._lock)

        when(self._path_mock).isfile(...).thenReturn(False)
        when(self._path_mock).isfile('default_location').thenReturn(True)

        self._subject = FileConfigurationLocker(
            file_locker=self._file_locker,
            os_lib=self._os_lib
        )

    def test_init(self):
        """ it can be instantiated """

        assert isinstance(self._subject, FileConfigurationLocker)
        assert isinstance(self._subject, ConfigurationLockerInterface)

    def test_is_default_for(self):
        """ it says if it’s the default for a given location """

        assert self._subject.is_default_for('default_location')
        assert not self._subject.is_default_for('other_location')

    def test_obtain_lock_shared(self):
        """ it can obtain a shared lock """

        expect(self._file_locker).Lock(
            'default_location', 'r+', timeout=5, flags=5
        ).thenReturn(self._lock)

        with self._subject.obtain_lock_shared('default_location') as file:
            assert self._file == file

        verifyNoUnwantedInteractions()
        verifyNoMoreInteractions()

    def test_obtain_lock_exclusive(self):
        """ it can obtain a exclusive lock """

        expect(self._file_locker).Lock(
            'default_location', 'w+', timeout=5, flags=6
        ).thenReturn(self._lock)

        with self._subject.obtain_lock_exclusive('default_location') as file:
            assert self._file == file

        verifyNoUnwantedInteractions()
        verifyNoMoreInteractions()
