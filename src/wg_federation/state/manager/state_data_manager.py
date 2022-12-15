from logging import Logger
from typing import Any

from wg_federation.crypto.wireguard_key_generator import WireguardKeyGenerator
from wg_federation.data.state.federation import Federation
from wg_federation.data.state.hq_state import HQState
from wg_federation.data.state.wireguard_interface import WireguardInterface
from wg_federation.data_transformation.configuration_location_finder import ConfigurationLocationFinder
from wg_federation.data_transformation.loader.can_load_configuration_interface import CanLoadConfigurationInterface
from wg_federation.data_transformation.locker.configuration_locker import ConfigurationLocker
from wg_federation.data_transformation.saver.can_save_configuration_interface import CanSaveConfigurationInterface
from wg_federation.event.hq.hq_event import HQEvent
from wg_federation.observer.event_dispatcher import EventDispatcher
from wg_federation.utils.utils import Utils


class StateDataManager:
    """
    Handles wg-federation HQState lifecycles: create, updates and reload form source of truth.
    """
    _configuration_location_finder: ConfigurationLocationFinder = None
    _configuration_loader: CanLoadConfigurationInterface = None
    _configuration_saver: CanSaveConfigurationInterface = None
    _configuration_locker: ConfigurationLocker = None
    _wireguard_key_generator: WireguardKeyGenerator = None
    _event_dispatcher: EventDispatcher = None
    _logger: Logger = None

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            configuration_location_finder: ConfigurationLocationFinder,
            configuration_loader: CanLoadConfigurationInterface,
            configuration_saver: CanSaveConfigurationInterface,
            configuration_locker: ConfigurationLocker,
            wireguard_key_generator: WireguardKeyGenerator,
            event_dispatcher: EventDispatcher,
            logger: Logger
    ):
        """
        Constructor
        :param configuration_location_finder:
        :param configuration_loader:
        :param configuration_saver:
        :param configuration_locker:
        :param wireguard_key_generator:
        :param event_dispatcher:
        :param logger:
        """
        self._configuration_location_finder = configuration_location_finder
        self._configuration_loader = configuration_loader
        self._configuration_saver = configuration_saver
        self._configuration_locker = configuration_locker
        self._wireguard_key_generator = wireguard_key_generator
        self._event_dispatcher = event_dispatcher
        self._logger = logger

    def reload(self) -> HQState:
        """
        Loads a HQState from the source of truth.
        :return:
        """
        with self._configuration_locker.lock_shared(self._configuration_location_finder.state()) as conf_file:
            raw_configuration = self._reload_from_source(conf_file)

        return self._event_dispatcher.dispatch([HQEvent.STATE_LOADED], HQState(
            federation=Federation.from_dict(raw_configuration.get('federation')),
            interfaces=WireguardInterface.from_list(raw_configuration.get('interfaces')),
            forums=WireguardInterface.from_list(raw_configuration.get('forums')),
            phone_lines=WireguardInterface.from_list(raw_configuration.get('phone_lines')),
        ))

    def create_hq_state(self) -> HQState:
        """
        Create a new HQState and save it.
        This method disregard whether a state already exists. To use with precaution.
        :return:
        """
        state = self._generate_new_hq_state()

        with self._configuration_locker.lock_exclusively(self._configuration_location_finder.state()) as conf_file:
            self._configuration_saver.save(state.dict(), conf_file)

        self._event_dispatcher.dispatch([HQEvent.STATE_CREATED], state)

        return state

    def _reload_from_source(self, source: Any = None) -> dict:
        self._logger.debug(
            f'{Utils.classname(self)}: reloading configuration from {self._configuration_location_finder.state()}'
        )

        return self._configuration_loader.load_if_exists(source)

    def _generate_new_hq_state(self) -> HQState:
        forum_key_pairs = self._wireguard_key_generator.generate_key_pairs()
        phone_line_key_pairs = self._wireguard_key_generator.generate_key_pairs()
        interface_key_pairs = self._wireguard_key_generator.generate_key_pairs()
        federation = Federation(name='wg-federation0')

        return HQState(
            federation=federation,
            forums=(
                WireguardInterface(
                    name='wgf-forum0',
                    addresses=('172.32.0.1/22',),
                    private_key=forum_key_pairs[0],
                    public_key=forum_key_pairs[1],
                    psk=self._wireguard_key_generator.generate_psk(),
                    listen_port=federation.forum_min_port,
                ),
            ),
            phone_lines=(
                WireguardInterface(
                    name='wgf-phoneline0',
                    addresses=('172.32.4.1/22',),
                    private_key=phone_line_key_pairs[0],
                    public_key=phone_line_key_pairs[1],
                    psk=self._wireguard_key_generator.generate_psk(),
                    listen_port=federation.phone_line_min_port,
                ),
            ),
            interfaces=(
                WireguardInterface(
                    name='wg-federation0',
                    addresses=('172.30.8.1/22',),
                    private_key=interface_key_pairs[0],
                    public_key=interface_key_pairs[1],
                    psk=self._wireguard_key_generator.generate_psk(),
                ),
            ),
        )
