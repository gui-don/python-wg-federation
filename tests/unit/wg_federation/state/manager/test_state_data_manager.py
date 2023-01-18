import pytest
from mockito import mock, unstub, verify, when, ANY, contains

from unit.wg_federation import hq_state
from wg_federation.data.input.command_line.secret_retreival_method import SecretRetrievalMethod
from wg_federation.data.state.hq_state import HQState
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.exception.user.data.state_signature_cannot_be_verified import StateNotBootstrapped
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

        when(self._configuration_loader).load_if_exists(self._file).thenReturn(hq_state().dict(exclude_defaults=True))
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
        """ it creates and saves a new HQState """

        self._subject.create_hq_state(self._user_input)

        verify(self._configuration_saver, times=1).save(ANY(dict), self._file)
        verify(self._event_dispatcher, times=1).dispatch([HQEvent.STATE_CREATED], ANY(HQState))

    def test_create_hq_state2(self):
        """ it raises a warning if the method for private key retrieval is insecure """

        self._user_input = mock({
            'private_key_retrieval_method': SecretRetrievalMethod.TEST_INSECURE_CLEARTEXT,
            'root_passphrase_command': 'example command',
        })

        self._subject.create_hq_state(self._user_input)

        verify(self._configuration_saver, times=1).save(ANY(dict), self._file)
        verify(self._event_dispatcher, times=1).dispatch([HQEvent.STATE_CREATED], ANY(HQState))
        verify(self._logger, times=1).warning(contains('The root passphrase retrieval method has been set to'))

    def test_create_hq_state3(self):
        """ it creates and saves a new HQState with WG_FEDERATION_ENV_VAR_OR_FILE method for secret retrieval """

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

    def test_reload2(self):
        """ it raises an error when trying to reload a state that was not bootstrapped """
        when(self._configuration_locker).lock_shared('state').thenRaise(FileNotFoundError)

        with pytest.raises(StateNotBootstrapped) as error:
            self._subject.reload()

        assert 'Unable to load the state: it was not bootstrapped. Run `hq boostrap`.' in str(error.value)
