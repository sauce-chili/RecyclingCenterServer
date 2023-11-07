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
class ApplicationForm:
    car_plate: str
    counterparty: str
    operation_type: str
    equipment_type: str
    camera_type: str
    scales_type: str
    weight_gross: float
    weight_extra: float
    weight_container: float
    weight_net: float
    url_photo: str
    date: datetime
    end_operations: bool


@dataclass
class ResultSaveApplication:
    url_photo: str
    weight_gross: float
    weight_net: float


@dataclass
class Order:
    counterparty: str
    car_plate: str


@dataclass
class Equipment:
    name: str


@dataclass
class IpCameraParam:
    url: str
    name: str


@dataclass
class ScalesParam:
    nameOrigin: str
    nameRu: str
    port: str


@dataclass
class WeighingResult:
    result: float
