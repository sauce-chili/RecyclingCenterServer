from pydantic.dataclasses import dataclass


@dataclass
class SaveApplicationResponse:
    weight_gross: float
    weight_net: float
    url_photo: str


@dataclass
class ScalesTypeResponse:
    nameEng: str
    nameRu: str


@dataclass
class OrderResponse:
    counterparty: str
    car_plates: list[str]


@dataclass
class EquipmentResponse:
    name: str
