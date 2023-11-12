from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class DatabaseParam:
    db_path: Path
    db_remote_path: Path
    image_buffer_folder_path: Path
    image_buffer_folder_remote_path: Path


@dataclass
class PreservationApplicationForm:
    """
    A class that stores the data necessary to save application form
    """
    car_plate: str
    counterparty: str
    operation_type: str
    equipment_type: str
    camera_type: str | None
    scales_type: str
    weight_extra: float
    weight_container: float


@dataclass
class ClosingApplication:
    car_plate: str
    counterparty: str
    equipment_type: str
    operation_type: str
    date: datetime


@dataclass
class ApplicationForm:
    car_plate: str
    counterparty: str
    operation_type: str
    equipment_type: str | None
    camera_type: str | None
    scales_type: str | None
    weight_gross: float | None
    weight_extra: float | None
    weight_container: float | None
    weight_net: float | None
    local_path_photo: Path | None
    date: datetime


@dataclass
class ResultSaveApplication:
    url_photo: str
    weight_gross: float
    weight_net: float


@dataclass
class Order:
    counterparty: str
    car_plates: set[str]


@dataclass
class Equipment:
    name: str


@dataclass
class IpCameraParam:
    url: str
    name: str

    def __hash__(self):
        return hash((self.url, self.name))

    def __eq__(self, other):
        if isinstance(other, IpCameraParam):
            return (self.url, self.name) == (other.url, other.name)
        return False


@dataclass
class ScalesParam:
    nameOrigin: str
    nameRu: str
    port: str

    def __hash__(self):
        return hash((self.nameOrigin, self.nameRu, self.port))

    def __eq__(self, other):
        if isinstance(other, ScalesParam):
            return (self.nameOrigin, self.nameRu, self.port) == (other.nameOrigin, other.nameRu, other.port)
        return False


@dataclass
class WeighingResult:
    result: float
