from types import ModuleType

import pytest
from mockito import mock, unstub, when

from wg_federation.data.input.configuration_backend import ConfigurationBackend
from wg_federation.data.input.user_input import UserInput
from wg_federation.data_transformation.configuration_location_finder import ConfigurationLocationFinder
from wg_federation.exception.user.data_transformation.configuration_backend_unsupported import \
    ConfigurationBackendUnsupported


class TestConfigurationLocationFinder:
    """ Test ConfigurationLocationFinder class """

    _user_input: UserInput = None
    _xdg_lib: ModuleType = None
    _pathlib_lib: ModuleType = None
    _application_name: str = 'testapp'

    _subject: ConfigurationLocationFinder = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._user_input = mock({
            'state_digest_backend': ConfigurationBackend.DEFAULT,
            'state_backend': ConfigurationBackend.FILE
        })

        self._pathlib_lib = mock()
        when(self._pathlib_lib).Path('/home/test', 'testapp', 'salt.txt').thenReturn('path_to_salt')

        self._xdg_lib = mock()
        when(self._xdg_lib).xdg_data_home().thenReturn('/home/test')
        when(self._xdg_lib).xdg_runtime_dir().thenReturn('/run')

        self._subject = ConfigurationLocationFinder(
            user_input=self._user_input,
            xdg_lib=self._xdg_lib,
            pathlib_lib=self._pathlib_lib,
            application_name=self._application_name,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, ConfigurationLocationFinder)

    def test_state_digest(self):
        """ it returns the state digest path location """
        self._user_input = mock({'state_digest_backend': ConfigurationBackend.FILE})
        when(self._pathlib_lib).Path('/home/test', 'testapp', 'state.digest').thenReturn('path_to_digest')

        self._subject = ConfigurationLocationFinder(
            user_input=self._user_input,
            xdg_lib=self._xdg_lib,
            pathlib_lib=self._pathlib_lib,
            application_name=self._application_name,
        )

        assert 'path_to_digest' == self._subject.state_digest()

    def test_state_digest2(self):
        """ it returns the state digest as same as state when user options sets state digest location to be DEFAULT """

        assert self._subject.state() == self._subject.state_digest()

    def test_state(self):
        """ it returns the state path """
        when(self._pathlib_lib).Path('/home/test', 'testapp', 'state.json').thenReturn('path_to_state')

        assert 'path_to_state' == self._subject.state_digest()

    def test_state2(self):
        """ it raises an error when the chosen ConfigurationBackend for state is not supported """
        self._user_input = mock({'state_backend': ConfigurationBackend.DEFAULT})

        self._subject = ConfigurationLocationFinder(
            user_input=self._user_input,
            xdg_lib=self._xdg_lib,
            pathlib_lib=self._pathlib_lib,
            application_name=self._application_name,
        )

        with pytest.raises(ConfigurationBackendUnsupported) as error:
            self._subject.state()

        assert 'is not supported for the state' in str(error)

    def test_state_digest_belongs_to_state(self):
        """ it returns whether or not the state digest belongs to the state """

        assert self._subject.state_digest_belongs_to_state()

        self._user_input = mock({'state_digest_backend': ConfigurationBackend.FILE})

        self._subject = ConfigurationLocationFinder(
            user_input=self._user_input,
            xdg_lib=self._xdg_lib,
            pathlib_lib=self._pathlib_lib,
            application_name=self._application_name,
        )

        assert not self._subject.state_digest_belongs_to_state()

    def test_salt(self):
        """ it returns the salt location """
        assert 'path_to_salt' == self._subject.salt()

    def test_salt2(self):
        """ it raises an error when the defined configurationBackend is unsupported for salt """
        self._user_input = mock({
            'state_backend': ConfigurationBackend.DEFAULT
        })

        self._subject = ConfigurationLocationFinder(
            user_input=self._user_input,
            xdg_lib=self._xdg_lib,
            pathlib_lib=self._pathlib_lib,
            application_name=self._application_name,
        )

        with pytest.raises(ConfigurationBackendUnsupported) as error:
            self._subject.salt()

        assert 'is not supported for the salt' in str(error)

    def test_interfaces_directory(self):
        """ it returns the wg interface directory """
        when(self._pathlib_lib).Path('/run', 'testapp', 'interfaces').thenReturn('path_to_interface')

        assert 'path_to_interface' == self._subject.interfaces_directory()

    def test_phone_lines_directory(self):
        """ it returns the wg phone lines directory """
        when(self._pathlib_lib).Path('/run', 'testapp', 'phone_lines').thenReturn('path_to_phone_lines')

        assert 'path_to_phone_lines' == self._subject.phone_lines_directory()

    def test_forums_directory(self):
        """ it returns the wg forums directory """
        when(self._pathlib_lib).Path('/run', 'testapp', 'forums').thenReturn('path_to_forums')

        assert 'path_to_forums' == self._subject.forums_directory()
