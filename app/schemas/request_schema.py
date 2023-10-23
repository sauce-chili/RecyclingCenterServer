from pydantic.dataclasses import dataclass


@dataclass
class SaveApplicationRequest:
    source: str | None
    destination: str | None
    type_operation: str
    type_equipment: str
    type_camera: str
    type_scale: str
