import logging
from enum import Enum

import pytest
from mockito import mock, when, unstub, verify, verifyNoMoreInteractions

from wg_federation.observer.event_dispatcher import EventDispatcher
from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.observer.status import Status


class EnumEvent(str, Enum):
    """ Enum for tests """
    EVENT1 = 1
    EVENT2 = 2
    EVENT3 = 3


class TestEventDispatcher:
    """ Test EventDispatcher class """

    _subscriber500: EventSubscriber = None
    _subscriber500bis: EventSubscriber = None
    _subscriber501: EventSubscriber = None
    _subscriber20: EventSubscriber = None
    _subscriber_stop: EventSubscriber = None

    _logger: logging.Logger = None

    _subject: EventDispatcher = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """

        self._logger = mock()
        when(self._logger).debug(...)
        when(self._logger).warning(...)

        self._subscriber500 = mock(EventSubscriber)
        when(self._subscriber500).get_order().thenReturn(500)
        when(self._subscriber500).must_stop_propagation().thenReturn(False)
        when(self._subscriber500).get_subscribed_events().thenReturn([EnumEvent.EVENT1])
        when(self._subscriber500).run(...).thenReturn(Status.SUCCESS)

        self._subscriber500bis = mock(EventSubscriber)
        when(self._subscriber500bis).get_order().thenReturn(500)
        when(self._subscriber500bis).must_stop_propagation().thenReturn(False)
        when(self._subscriber500bis).get_subscribed_events().thenReturn([EnumEvent.EVENT2])
        when(self._subscriber500bis).run(...).thenReturn(Status.SUCCESS)

        self._subscriber501 = mock(EventSubscriber)
        when(self._subscriber501).get_order().thenReturn(501)
        when(self._subscriber501).must_stop_propagation().thenReturn(False)
        when(self._subscriber501).get_subscribed_events().thenReturn([EnumEvent.EVENT3, EnumEvent.EVENT1])
        when(self._subscriber501).run(...).thenReturn(Status.SUCCESS)

        self._subscriber20 = mock(EventSubscriber)
        when(self._subscriber20).get_order().thenReturn(20)
        when(self._subscriber20).must_stop_propagation().thenReturn(False)
        when(self._subscriber20).get_subscribed_events().thenReturn([EnumEvent.EVENT1, EnumEvent.EVENT2])
        when(self._subscriber20).run(...).thenReturn(Status.DEFAULT_ERROR)

        self._subscriber_stop = mock(EventSubscriber)
        when(self._subscriber_stop).get_order().thenReturn(10)
        when(self._subscriber_stop).must_stop_propagation().thenReturn(True)
        when(self._subscriber_stop).get_subscribed_events().thenReturn([EnumEvent.EVENT2])
        when(self._subscriber_stop).run(...).thenReturn(Status.SUCCESS)

        self._subject = EventDispatcher(
            logger=self._logger,
            subscribers=[self._subscriber500, self._subscriber20, self._subscriber501, self._subscriber500bis]
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, EventDispatcher)

    def test_init2(self):
        """ it registers subscribers outside the constructor """
        _subject = EventDispatcher(
            logger=self._logger,
        )
        self._subject.register(self._subscriber501)
        self._subject.register(self._subscriber500bis)
        self._subject.register(self._subscriber20)
        self._subject.register(self._subscriber500)

        assert isinstance(_subject, EventDispatcher)

    def test_dispatch(self):
        """ it runs subscriber listening to the dispatched events """
        self._subject.dispatch([EnumEvent.EVENT1, EnumEvent.EVENT3], 'data')

        verify(self._subscriber20, times=1).run('data')
        verify(self._subscriber500, times=1).run('data')
        verify(self._subscriber501, times=1).run('data')
        verify(self._subscriber500bis, times=0).run(...)

        verify(self._logger, times=1).warning('“EventSubscriber♦” failed.')

        verifyNoMoreInteractions()

    def test_dispatch2(self):
        """ it stops the propagation after running a subscriber that requires it """
        self._subject.register(self._subscriber_stop)
        self._subject.dispatch([EnumEvent.EVENT2], 'data')

        verify(self._subscriber_stop, times=1).run('data')
        verify(self._subscriber20, times=0).run(...)
        verify(self._subscriber500, times=0).run(...)
        verify(self._subscriber501, times=0).run(...)
        verify(self._subscriber500bis, times=0).run(...)
