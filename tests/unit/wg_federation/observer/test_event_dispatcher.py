import logging
from enum import Enum

import pytest
from mockito import mock, when, unstub, verify, verifyNoMoreInteractions, contains

from wg_federation.observer.error.subscriber_graceful_error import SubscriberGracefulError
from wg_federation.observer.event_dispatcher import EventDispatcher
from wg_federation.observer.event_subscriber import EventSubscriber


class EnumEvent(Enum):
    """ Enum for tests """
    EVENT = ('event', str)
    EVENT_MUTABLE = ('event', str, True)
    EVENT_BIS = ('event_bis', str, False)
    EVENT_INVALID = 'invalid'
    EVENT_EMPTY = ('empty', str)


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
        when(self._subscriber500).get_subscribed_events().thenReturn([EnumEvent.EVENT])
        when(self._subscriber500).should_run(...).thenReturn(True)
        when(self._subscriber500).run(...).thenReturn('modified')

        self._subscriber500bis = mock(EventSubscriber)
        when(self._subscriber500bis).get_order().thenReturn(500)
        when(self._subscriber500bis).must_stop_propagation().thenReturn(False)
        when(self._subscriber500bis).get_subscribed_events().thenReturn([EnumEvent.EVENT_MUTABLE])
        when(self._subscriber500bis).should_run(...).thenReturn(True)
        when(self._subscriber500bis).run(...).thenReturn('modified')

        self._subscriber501 = mock(EventSubscriber)
        when(self._subscriber501).get_order().thenReturn(501)
        when(self._subscriber501).must_stop_propagation().thenReturn(False)
        when(self._subscriber501).get_subscribed_events().thenReturn([EnumEvent.EVENT_BIS, EnumEvent.EVENT])
        when(self._subscriber501).should_run(...).thenReturn(True)
        when(self._subscriber501).run(...).thenReturn('modified')

        self._subscriber20 = mock(EventSubscriber)
        when(self._subscriber20).get_order().thenReturn(20)
        when(self._subscriber20).must_stop_propagation().thenReturn(False)
        when(self._subscriber20).get_subscribed_events().thenReturn([EnumEvent.EVENT, EnumEvent.EVENT_MUTABLE])
        when(self._subscriber20).should_run(...).thenReturn(True)
        when(self._subscriber20).should_run('not').thenReturn(False)
        when(self._subscriber20).run(...).thenReturn('modified')

        self._subscriber_stop = mock(EventSubscriber)
        when(self._subscriber_stop).get_order().thenReturn(10)
        when(self._subscriber_stop).must_stop_propagation().thenReturn(True)
        when(self._subscriber_stop).get_subscribed_events().thenReturn([EnumEvent.EVENT])
        when(self._subscriber_stop).should_run(...).thenReturn(True)
        when(self._subscriber_stop).run(...).thenReturn('modified')

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
        self._subject.dispatch([EnumEvent.EVENT, EnumEvent.EVENT_BIS], 'data')
        verify(self._logger, times=1).debug('Dispatching “event, event_bis” events.')

        verify(self._subscriber20, times=1).run('data')
        verify(self._subscriber500, times=1).run('data')
        verify(self._subscriber501, times=1).run('data')
        verify(self._subscriber500bis, times=0).run(...)

        verify(self._logger, times=2).debug(
            'EventSubscriber♦ was run in response to: “event”. Allowing mutable data? False.'
        )

        verifyNoMoreInteractions()

    def test_dispatch2(self):
        """ it ignores invalid events but still dispatches valid ones """
        self._subject.dispatch([EnumEvent.EVENT_INVALID, EnumEvent.EVENT_BIS], 'data')

        verify(self._subscriber20, times=0).run(...)
        verify(self._subscriber500, times=0).run(...)
        verify(self._subscriber501, times=1).run('data')
        verify(self._subscriber500bis, times=0).run(...)

        verify(self._logger, times=1).warning(contains('An event named “EnumEvent.EVENT_INVALID” is invalid,'))

        verifyNoMoreInteractions()

    def test_dispatch3(self):
        """ it ignores events with no subscriber listening to it """
        self._subject.dispatch([EnumEvent.EVENT_EMPTY], 'data')

        verify(self._subscriber20, times=0).run(...)
        verify(self._subscriber500, times=0).run(...)
        verify(self._subscriber501, times=0).run(...)
        verify(self._subscriber500bis, times=0).run(...)

        verify(self._logger, times=0).warning(...)

        verifyNoMoreInteractions()

    def test_dispatch4(self):
        """ it ignores dispatched event with no matching data types """
        self._subject.dispatch([EnumEvent.EVENT], 123)

        verify(self._subscriber20, times=0).run(...)
        verify(self._subscriber500, times=0).run(...)
        verify(self._subscriber501, times=0).run(...)
        verify(self._subscriber500bis, times=0).run(...)

        verify(self._logger, times=3).warning(contains(' Dispatched events do not support type “<class \'int\'>”.'))

        verifyNoMoreInteractions()

    def test_dispatch5(self):
        """ it ignores subscriber that should not run """
        self._subject.dispatch([EnumEvent.EVENT], 'not')

        verify(self._subscriber20, times=0).run(...)
        verify(self._subscriber500, times=1).run('not')
        verify(self._subscriber501, times=1).run('not')
        verify(self._subscriber500bis, times=0).run(...)

        verify(self._logger, times=1).debug('EventSubscriber♦ was skipped.')

        verifyNoMoreInteractions()

    def test_dispatch6(self):
        """ it allows mutation for specific event and subscribers """
        assert 'modified' == self._subject.dispatch([EnumEvent.EVENT, EnumEvent.EVENT_MUTABLE], 'data')

        verify(self._subscriber20, times=1).run('data')
        verify(self._subscriber500, times=1).run('data')
        verify(self._subscriber500bis, times=1).run('data')  # This subscriber mutates
        verify(self._subscriber501, times=1).run('modified')

        verify(self._logger, times=0).warning(...)

        verifyNoMoreInteractions()

    def test_dispatch7(self):
        """ it logs a warning if any subscriber raise a specific error """

        when(self._subscriber20).run('data').thenRaise(SubscriberGracefulError('error!'))

        self._subject.dispatch([EnumEvent.EVENT], 'data')

        verify(self._subscriber20, times=1).run('data')
        verify(self._subscriber500, times=1).run('data')
        verify(self._subscriber500bis, times=0).run(...)
        verify(self._subscriber501, times=1).run('data')

        verify(self._logger, times=1).warning(contains('This error was raised: error!'))

        verifyNoMoreInteractions()

    def test_dispatch8(self):
        """ it stops propagation to any other subscriber if option is set """

        self._subject.register(self._subscriber_stop)

        self._subject.dispatch([EnumEvent.EVENT], 'data')

        verify(self._subscriber_stop, times=1).run('data')
        verify(self._subscriber20, times=0).run(...)
        verify(self._subscriber500, times=0).run(...)
        verify(self._subscriber500bis, times=0).run(...)
        verify(self._subscriber501, times=0).run(...)

        verify(self._logger, times=1).debug(contains('Stopping event propagation'))

        verifyNoMoreInteractions()
