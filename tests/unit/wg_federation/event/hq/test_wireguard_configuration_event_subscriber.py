import pytest
from mockito import unstub

from wg_federation.data.state.wireguard_interface import WireguardInterface
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.event.hq.wireguard_configuration_event_subscriber import WireguardConfigurationEventSubscriber
from wg_federation.observer.event_subscriber import EventSubscriber


class TestWireguardConfigurationEventSubscriber:
    """ Test WireguardConfigurationEventSubscriber class """

    _subject: WireguardConfigurationEventSubscriber = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """

        self._subject = WireguardConfigurationEventSubscriber()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, EventSubscriber)

    def test_get_subscribed_events(self):
        """ it returns subscribed events """
        assert HQEvent.STATE_CREATED in self._subject.get_subscribed_events()
        assert HQEvent.STATE_BEFORE_UPDATE in self._subject.get_subscribed_events()
        assert HQEvent.STATE_UPDATED in self._subject.get_subscribed_events()

    def test_get_order(self):
        """ it returns its order of execution """
        assert 500 == self._subject.get_order()

    def test_must_stop_propagation(self):
        """ it returns whether or not it should stop propagation """
        assert not self._subject.must_stop_propagation()

    def test_run(self):
        """ it runs """
        assert isinstance(self._subject.run(WireguardInterface(
            private_key='9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
            public_key='1OAiqIBY7Xx7OxjWVBXzPFKDfLNY1SOnTYyBJDaAaxs=',
        )), WireguardInterface)
