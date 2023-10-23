from pydantic.dataclasses import dataclass


@dataclass
class SaveApplicationResponse:
    weight: float
    id_record: int
    url_photo: str
