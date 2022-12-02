from enum import Enum
from typing import Any

from wg_federation.data_transformation.saver.can_save_configuration_interface import CanSaveConfigurationInterface
from wg_federation.utils.utils import Utils


class MutableTransformConfigurationSaverProxy(CanSaveConfigurationInterface):
    """
    CanSaveConfigurationInterface Proxy.
    Able to transform data with immutable types to mutable.
    """

    _configuration_saver: CanSaveConfigurationInterface = None

    def __init__(self, configuration_saver: CanSaveConfigurationInterface):
        """
        Constructor
        :param configuration_saver:
        """
        self._configuration_saver = configuration_saver

    def save_try(self, data: dict, destination: Any, configuration_saver: type = None) -> None:
        self._configuration_saver.save_try(
            dict(Utils.recursive_map(self._transform_mutable, data)),
            destination,
            configuration_saver
        )

    def save(self, data: dict, destination: Any, configuration_saver: type = None) -> None:
        self._configuration_saver.save(
            dict(Utils.recursive_map(self._transform_mutable, data)),
            destination,
            configuration_saver
        )

    def _transform_mutable(self, item: Any) -> Any:
        if isinstance(item, (tuple, set, frozenset,)):
            return list(item)
        if isinstance(item, Enum):
            return item.value

        return item
