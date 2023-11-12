from dataclasses import dataclass


@dataclass
class PreservationApplicationDto:
    car_plate: str
    counterparty: str
    operation_type: str | None
    equipment_type: str | None
    camera_type: str | None
    scales_type: str | None
    weight_gross: float | None
    weight_extra: float | None
    weight_container: float | None
    weight_net: float | None
    url_photo: str | None
    date: str
    end_weighing: int


# @dataclass
# class ActiveApplicationStorageDto:
#     weighing_order: int
#     source: str
#     destination: str
#     type_operation: str
#     type_equipment: str
#     type_camera: str
#     type_scales: str
#     weight: float
#     url_photo: str
#     date: str


# @dataclass
# class ApplicationStorageDto:
#     id: int
#     weighing_order: int
#     source: str
#     destination: str
#     type_operation: str
#     type_equipment: str
#     type_camera: str
#     type_scales: str
#     weight: float
#     url_photo: str
#     date: str

@dataclass
class ApplicationStorageDto:
    id: str
    car_plate: str
    counterparty: str
    operation_type: str | None
    equipment_type: str | None
    camera_type: str | None
    scales_type: str | None
    weight_gross: float | None
    weight_container: float | None
    weight_extra: float | None
    weight_net: float | None
    url_photo: str | None
    date: str
    end_weighing: int
