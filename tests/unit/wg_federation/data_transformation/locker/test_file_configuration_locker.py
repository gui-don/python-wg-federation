import pytest
from mockito import mock, unstub, when, expect, verifyNoUnwantedInteractions, verifyNoMoreInteractions
from portalocker import LockFlags

from wg_federation.data_transformation.locker.configuration_locker_interface import ConfigurationLockerInterface
from wg_federation.data_transformation.locker.file_configuration_locker import FileConfigurationLocker

# irrelevant in a test class
# pylint: disable=too-many-instance-attributes


class TestFileConfigurationLocker:
    """ Test FileConfigurationLocker class """

    _file = None
    _lock = None
    _file_locker = None
    _parent_path = None
    _parent_path_not_exist = None
    _path_mock = None
    _path_mock_not_exist = None
    _path_lib = None

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

        # pylint: disable=unnecessary-dunder-call
        when(self._lock).__enter__(...).thenReturn(self._file)
        when(self._lock).__exit__(...).thenReturn(self._file)

        self._file_locker = mock({'LockFlags': LockFlags})

        self._parent_path = mock()
        when(self._parent_path).is_dir().thenReturn(True)

        self._parent_path_not_exist = mock()
        when(self._parent_path_not_exist).is_dir().thenReturn(False)

        self._path_mock = mock({'parent': self._parent_path})
        self._path_mock_not_exist = mock({'parent': self._parent_path_not_exist})

        self._path_lib = mock()
        when(self._path_lib).Path(...).thenReturn(self._path_mock_not_exist)
        when(self._path_lib).Path('default_location').thenReturn(self._path_mock)

        when(self._file_locker).Lock(...).thenReturn(self._lock)

        self._subject = FileConfigurationLocker(
            file_locker=self._file_locker,
            path_lib=self._path_lib
        )

    def test_init(self):
        """ it can be instantiated """

        assert isinstance(self._subject, FileConfigurationLocker)
        assert isinstance(self._subject, ConfigurationLockerInterface)

    def test_is_default_for(self):
        """ it says if it’s the default for a given location """

        assert self._subject.is_default_for('default_location')
        assert not self._subject.is_default_for('other_location')

    def test_obtain_shared_lock(self):
        """ it can obtain a shared lock """

        expect(self._file_locker).Lock(
            'default_location', 'r+', timeout=5, flags=5
        ).thenReturn(self._lock)

        with self._subject.obtain_shared_lock('default_location') as file:
            assert self._file == file

        verifyNoUnwantedInteractions()
        verifyNoMoreInteractions()

    def test_obtain_exclusive_lock(self):
        """ it can obtain a exclusive lock """

        expect(self._file_locker).Lock(
            'default_location', 'w+', timeout=5, flags=6
        ).thenReturn(self._lock)

        with self._subject.obtain_exclusive_lock('default_location') as file:
            assert self._file == file

        verifyNoUnwantedInteractions()
        verifyNoMoreInteractions()
