import pytest
from mockito import mock, unstub, verify, when, ANY, contains

from wg_federation.data.input.command_line.secret_retreival_method import SecretRetrievalMethod
from wg_federation.data.state.hq_state import HQState
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.state.manager.state_data_manager import StateDataManager


class TestStateDataManager:
    """ Test StateDataManager class """

    _file = None
    _lock = None
    _user_input = None

    _configuration_location_finder = None
    _configuration_loader = None
    _configuration_saver = None
    _configuration_locker = None
    _wireguard_key_generator = None
    _event_dispatcher = None
    _logger = None

    _subject: StateDataManager = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.init()

    def init(self):
        """ Constructor """

        self._user_input = mock({
            'private_key_retrieval_method': SecretRetrievalMethod.WG_FEDERATION_COMMAND,
            'root_passphrase_command': 'example command',
        })

        self._lock = mock()
        # pylint: disable=unnecessary-dunder-call
        when(self._lock).__enter__(...).thenReturn(self._file)
        when(self._lock).__exit__(...).thenReturn(self._file)

        self._configuration_location_finder = mock()
        when(self._configuration_location_finder).state().thenReturn('state')

        self._configuration_loader = mock()
        when(self._configuration_loader).load_if_exists(self._file).thenReturn(
            {'federation': {'name': 'wg-federation0',
                            'forum_max_port': 44299,
                            'forum_min_port': 44200,
                            'phone_line_max_port': 44199,
                            'phone_line_min_port': 44100},
             'forums': [{'address': ['172.30.0.1/22'],
                         'listen_port': 44200,
                         'mtu': None,
                         'name': 'wgf-forum0',
                         'status': 'NEW',
                         'public_key': '2a9+BiAk3oQHOqSwUf2sfyUs9SOkm1TwnkAKk0cbPFg=',
                         'private_key': 'qdYplAbCzmsK938SBfzLdttcloK18+77q1M+TWJpnVk=',
                         'shared_psk': 'mHZFMxgZ+frxa3CtZewdrH3E5o2RwwNbs49wyaf+EnY='}],
             'phone_lines': [{'address': ['172.30.4.1/22'],
                              'listen_port': 44100,
                              'mtu': None,
                              'name': 'wgf-phoneline0',
                              'status': 'NEW',
                              'public_key': '785FGWX5b/nvr8a40YwBTz/h34Fu8sJeDSTSMCCW/nw=',
                              'private_key': '0MQX95OV9b05zkAmyzJMvseCm87aXt9vEmTTBqbOwrg=',
                              'shared_psk': '3No0+mBhyBP8+6z1xrgy7navwT2xZuXWywzn8UgP6Ik='}],
             'interfaces': [{'address': ['172.30.8.1/22'],
                             'listen_port': 35200,
                             'mtu': None,
                             'name': 'wg-federation0',
                             'status': 'NEW',
                             'public_key': 'tmX9goa9jAABptDQ9PDsb+Xd5++HZRS3nwBDExckWzU=',
                             'private_key': 'P6dlK8fhauCwOkwvyp6SOKP8sftuX8JKQVNbL1O8iS8=',
                             'shared_psk': 'YiUz3hI9RAr+Mo4CkHMgIG7aNpbSWG76ZXBxjvGAkG8='}]})
        self._configuration_saver = mock()

        self._configuration_locker = mock()
        when(self._configuration_locker).lock_exclusively('state').thenReturn(self._lock)
        when(self._configuration_locker).lock_shared('state').thenReturn(self._lock)

        self._wireguard_key_generator = mock()
        when(self._wireguard_key_generator).generate_key_pairs().thenReturn(
            ('TEJkUEP2p2RxXlAKshLgZLwnIAAOhFzNeJhv6wvSxkY=', 'pifGr/4QrabUT9HvzMhYoqTZiZAF1R2kB3d5TU1jLCw='),
            ('2EJkUEP2p2RxXlAKshLgZLwnIAAOhFzNeJhv6wvSxkY=', '2ifGr/4QrabUT9HvzMhYoqTZiZAF1R2kB3d5TU1jLCw='),
            ('3EJkUEP2p2RxXlAKshLgZLwnIAAOhFzNeJhv6wvSxkY=', '3ifGr/4QrabUT9HvzMhYoqTZiZAF1R2kB3d5TU1jLCw='),
        )
        when(self._wireguard_key_generator).generate_psk().thenReturn(
            'pBdexuVBGPb1Rrqk/DfH9JTp95V+li7WwTKigmiuCQc=',
            'q6RUpn6g/iz+c4rQsixD+UMa39n+8NxaVJ70ykYlgkA=',
            'icpKkwUPFcduokh8jTU4iAoLDwCrk9Z+TCAHckmYXH8=',
        )

        self._event_dispatcher = mock()

        self._logger = mock()

        self._subject = StateDataManager(
            configuration_location_finder=self._configuration_location_finder,
            configuration_loader=self._configuration_loader,
            configuration_saver=self._configuration_saver,
            configuration_locker=self._configuration_locker,
            wireguard_key_generator=self._wireguard_key_generator,
            event_dispatcher=self._event_dispatcher,
            logger=self._logger,
        )

    def test_init(self):
        """ it can be instantiated """

        assert isinstance(self._subject, StateDataManager)

    def test_create_hq_state(self):
        """ it creates and save a new HQState """

        self._subject.create_hq_state(self._user_input)

        verify(self._configuration_saver, times=1).save(ANY(dict), self._file)
        verify(self._event_dispatcher, times=1).dispatch([HQEvent.STATE_CREATED], ANY(HQState))

    def test_create_hq_state2(self):
        """ it raise a warning if the method for private key retrieval is insecure """

        self._user_input = mock({
            'private_key_retrieval_method': SecretRetrievalMethod.TEST_INSECURE_CLEARTEXT,
            'root_passphrase_command': 'example command',
        })

        self._subject.create_hq_state(self._user_input)

        verify(self._configuration_saver, times=1).save(ANY(dict), self._file)
        verify(self._event_dispatcher, times=1).dispatch([HQEvent.STATE_CREATED], ANY(HQState))
        verify(self._logger, times=1).warning(contains('The root passphrase retrieval method has been set to'))

    def test_create_hq_state3(self):
        """ it creates and save a new HQState with WG_FEDERATION_ENV_VAR_OR_FILE method for secret retrieval """

        self._user_input = mock({
            'private_key_retrieval_method': SecretRetrievalMethod.WG_FEDERATION_ENV_VAR_OR_FILE,
            'root_passphrase_command': 'example command',
        })

        self._subject.create_hq_state(self._user_input)

        verify(self._configuration_saver, times=1).save(ANY(dict), self._file)
        verify(self._event_dispatcher, times=1).dispatch([HQEvent.STATE_CREATED], ANY(HQState))
        verify(self._logger, times=0).warning(...)

    def test_reload(self):
        """ it reloads the state from default source """

        self._subject.reload()

        verify(self._configuration_loader, times=1).load_if_exists(self._file)
        verify(self._event_dispatcher, times=1).dispatch([HQEvent.STATE_LOADED], ANY(HQState))
