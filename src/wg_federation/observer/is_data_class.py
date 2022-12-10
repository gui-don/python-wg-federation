from typing import Dict, Protocol


class IsDataClass(Protocol):
    """
    Represents any kind of data class
    """
    __dataclass_fields__: Dict
