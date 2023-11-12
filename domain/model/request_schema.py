from pydantic.dataclasses import dataclass


@dataclass
class SaveApplicationRequest:
    car_plate: str
    counterparty: str
    operation_type: str
    equipment_type: str
    camera_type: str | None
    scales_type: str
    weight_extra: float
    weight_container: float


@dataclass
class SaveApplicationOfEndWeightingRequest:
    car_plate: str
    counterparty: str
    operation_type: str
    equipment_type: str
