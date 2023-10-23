from dataclasses import dataclass


@dataclass
class SaveActiveApplicationDto:
    source: str
    destination: str
    type_operation: str
    camera_type: str
    scales_type: str
    weight: float
    url_photo: str
    date: str


@dataclass
class ActiveApplicationDto:
    weighing_order: int
    source: str
    destination: str
    type_operation: str
    camera_type: str
    scales_type: str
    weight: float
    url_photo: str
    date: str


@dataclass
class ApplicationDto:
    id: int
    weighing_order: int
    source: str
    destination: str
    type_operation: str
    camera_type: str
    scales_type: str
    weight: float
    url_photo: str
    date: str
