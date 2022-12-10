from enum import Enum

import pytest
from mockito import unstub
from pydantic import BaseModel

from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.observer.is_data_class import IsDataClass
from wg_federation.observer.status import Status


class DummyData(BaseModel):
    """ Dummy data for tests """
    value: str = 'default'


class DummyEventSubscriber(EventSubscriber):
    """ Dummy EventSubscriber for tests """

    def get_subscribed_events(self) -> list[Enum]:
        return [Status.SUCCESS]

    def _do_run(self, data: IsDataClass) -> Status:
        return Status.SUCCESS

    @classmethod
    def support_data_class(cls) -> type:
        return DummyData


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

        self._subject = DummyEventSubscriber()

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, EventSubscriber)

    def test_support_data_class(self):
        """ it returns what kind of data class it supports """
        assert DummyData == self._subject.support_data_class()

    def test_get_subscribed_events(self):
        """ it returns subscribed events """
        assert [Status.SUCCESS] == self._subject.get_subscribed_events()

    def test_get_order(self):
        """ it returns its order of execution """
        assert 500 == self._subject.get_order()

    def test_must_stop_propagation(self):
        """ it returns whether or not it should stop propagation """
        assert not self._subject.must_stop_propagation()

    def test_run(self):
        """ it runs """
        assert Status.SUCCESS == self._subject.run(DummyData())

    def test_run2(self):
        """ it throws an exception if run with the wrong type of data """
        with pytest.raises(RuntimeError) as error:
            self._subject.run('wrong_data')

        assert 'responded to an event with unsupported data type' in str(error)
