from pydantic.dataclasses import dataclass


@dataclass
class ApplicationForm:
    """
    class storing already saved application form data
    """
    id: int
    weighing_order: int  # This number is order of weighting in within one waybill
    source: str
    destination: str
    type_operation: str
    camera_type: str
    scales_type: str
    weight: float
    url_photo: str


@dataclass
class SaveApplicationForm:
    """
    A class that stores the data necessary to save application form
    """
    source: str | None
    destination: str | None
    type_operation: str
    type_equipment: str
    type_camera: str
    type_scale: str


@dataclass
class Waybill:
    id: str


@dataclass
class Equipment:
    name: str


@dataclass
class IpCameraParam:
    ip: str
    name: str


@dataclass
class ScalesParam:
    nameOrigin: str
    nameRu: str
    port: str


@dataclass
class WeighingResult:
    weight: float
