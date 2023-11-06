from pydantic.dataclasses import dataclass


@dataclass
class SaveApplicationResponse:
    weight_gross: float
    weight_net: float
    url_photo: str
