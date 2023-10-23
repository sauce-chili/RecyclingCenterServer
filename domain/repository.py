from typing import Protocol
from domain.models import *


class LocalRepository(Protocol):

    def save_application(self, application_form: ApplicationForm) -> None:
        ...

    def save_waybill(self) -> None:
        ...


class RemoteRepository(Protocol):

    def upload(self) -> None:
        ...


class CameraParamsRepository(Protocol):

    def get_cameras_list(self) -> list[IpCameraParam]:
        ...

    def get_camera_parameters_by_name(self, name: str) -> IpCameraParam:
        ...

    def get_camera_parameters_by_ip(self, ip: str) -> IpCameraParam:
        ...


class ScalesParamsRepository(Protocol):

    def get_scales_list(self) -> list[ScalesParam]:
        ...

    def get_scales_by_name(self, name: str) -> ScalesParam:
        ...


class WaybillsRepository(Protocol):

    def get_intake_waybills(self) -> list[Waybill]:
        ...

    def get_release_waybills(self) -> list[Waybill]:
        ...

    def get_movement_waybills(self) -> list[Waybill]:
        ...


class EquipmentsRepository(Protocol):

    def get_equipment_types(self) -> list[Equipment]:
        ...
