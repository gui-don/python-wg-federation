from types import ModuleType

import pytest
from mockito import unstub, mock, when, ANY, verify, patch

from unit.wg_federation import hq_state
from wg_federation.data.state.hq_state import HQState
from wg_federation.data_transformation.configuration_location_finder import ConfigurationLocationFinder
from wg_federation.data_transformation.locker.configuration_locker import ConfigurationLocker
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.event.hq.wireguard_interface_configuration_event_subscriber import WireguardInterfaceConfigurationEventSubscribe
from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.utils.utils import Utils


class TestWireguardConfigurationEventSubscriber:
    """ Test WireguardConfigurationEventSubscriber class """

    _os_path = None
    _file = None
    _lock = None
    _hq_state: HQState = None

    _os_lib: ModuleType = None
    _configuration_location_finder: ConfigurationLocationFinder = None
    _configuration_locker: ConfigurationLocker = None
    _subject: WireguardInterfaceConfigurationEventSubscribe = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """
        self._hq_state = hq_state()

        self._file = mock()

        self._lock = mock()
        # pylint: disable=unnecessary-dunder-call
        when(self._lock).__enter__(...).thenReturn(self._file)
        when(self._lock).__exit__(...).thenReturn(self._file)

        self._os_path = mock()
        when(self._os_path).join('forum_dir', ANY).thenReturn('forum_fullpath')
        when(self._os_path).join('interface_dir', ANY).thenReturn('interface_fullpath')
        when(self._os_path).join('phone_line_dir', ANY).thenReturn('phone_line_fullpath')

        self._configuration_locker = mock()
        when(self._configuration_locker).lock_exclusively(ANY).thenReturn(self._lock)

        self._configuration_location_finder = mock()
        when(self._configuration_location_finder).forums_directory().thenReturn('forum_dir')
        when(self._configuration_location_finder).interfaces_directory().thenReturn('interface_dir')
        when(self._configuration_location_finder).phone_lines_directory().thenReturn('phone_line_dir')

        self._os_lib = mock({'path': self._os_path})

        self._subject = WireguardInterfaceConfigurationEventSubscribe(
            os_lib=self._os_lib,
            configuration_location_finder=self._configuration_location_finder,
            configuration_locker=self._configuration_locker,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, EventSubscriber)
        assert isinstance(self._subject, WireguardInterfaceConfigurationEventSubscribe)

    def test_get_subscribed_events(self):
        """ it returns subscribed events """
        assert HQEvent.STATE_CREATED in self._subject.get_subscribed_events()
        assert HQEvent.STATE_UPDATED in self._subject.get_subscribed_events()

    def test_get_order(self):
        """ it returns its order of execution """
        assert 500 == self._subject.get_order()

    def test_must_stop_propagation(self):
        """ it returns whether or not it should stop propagation """
        assert not self._subject.must_stop_propagation()

    def test_run(self):
        """ it creates all wireguard configuration files for all interfaces """
        patch(Utils.open, lambda x, y, z: self._lock)

        result = self._subject.run(self._hq_state)

        assert self._hq_state == result

        verify(self._configuration_locker.lock_exclusively('forum_fullpath'), times=1)
        verify(self._configuration_locker.lock_exclusively('interface_fullpath'), times=1)
        verify(self._configuration_locker.lock_exclusively('phone_line_fullpath'), times=1)
