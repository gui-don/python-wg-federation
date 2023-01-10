from enum import Enum

import pytest
from mockito import unstub
from pydantic import BaseModel

from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.observer.is_data_class import IsDataClass


class DummyData(BaseModel):
    """ Dummy data for tests """
    value: str = 'default'


class DummyEvent(Enum):
    """ Dummy event for tests """
    TEST = ('test', DummyData, True)


class DummyEventSubscriber(EventSubscriber[IsDataClass]):
    """ Dummy EventSubscriber for tests """

    _order = None

    def __init__(self, order):
        self._order = order

    def get_subscribed_events(self) -> list[Enum]:
        return [DummyEvent.TEST]

    def run(self, data: IsDataClass) -> IsDataClass:
        data.value = 'modified'
        return data

    def get_order(self) -> int:
        return self._order


class TestEventSubscriber:
    """ Test EventSubscriber class """

    _subject: EventSubscriber = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """

        self._subject = DummyEventSubscriber(500)

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, EventSubscriber)

    def test_get_subscribed_events(self):
        """ it returns subscribed events """
        assert [DummyEvent.TEST] == self._subject.get_subscribed_events()

    def test_get_subscribed_events2(self):
        """ it raises an error if get_subscribed_events is not implemented """
        with pytest.raises(NotImplementedError):
            EventSubscriber().get_subscribed_events()

    def test_get_order(self):
        """ it returns its default order of execution """
        assert 500 == self._subject.get_order()

    def test_get_order2(self):
        """ it returns its order of execution """
        assert 34 == DummyEventSubscriber(34).get_order()

    def test_must_stop_propagation(self):
        """ it returns whether it should stop propagation """
        assert not self._subject.must_stop_propagation()

    def test_run(self):
        """ it runs and can change data object """
        data = DummyData()
        assert 'default' == data.value
        assert data == self._subject.run(data)
        assert 'modified' == data.value

    def test_run2(self):
        """ it raises an error if EventSubscriber does not implement run """
        with pytest.raises(NotImplementedError):
            EventSubscriber().run('any')

    def test_should_run(self):
        """ it does run by default """
        assert self._subject.should_run(DummyData())
