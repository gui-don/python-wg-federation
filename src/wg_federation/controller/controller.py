from wg_federation.data.input.user_input import UserInput
from wg_federation.observer.event_subscriber import EventSubscriber
from wg_federation.observer.is_data_class import IsDataClass
from wg_federation.observer.status import Status
from wg_federation.utils.utils import Utils


class Controller(EventSubscriber):
    """
    Abstract Controller class
    """

    def run(self, data: IsDataClass) -> Status:
        result = super().run(data)
        if result not in [Status.SUCCESS, Status.NOT_RUN]:
            raise RuntimeError(f'{Utils.classname(self)} failed with status code {result}')

        return result

    @classmethod
    def support_data_class(cls) -> type:
        return UserInput
