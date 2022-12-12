from pydantic import BaseModel


class IsDataClass(BaseModel):
    """
    Represents any kind of data class
    """
    # __dataclass_fields__: Dict
