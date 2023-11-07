from typing import Protocol
from domain.models import *


class ApplicationRepository(Protocol):

    def save_application(self, application_form: ApplicationForm) -> None:
        ...

    def close_application(self, application_from: ApplicationForm) -> None:
        ...


class RemoteRepository(Protocol):

    def update_db(self) -> None:
        ...

    def upload_photo(self, path_to_photo: Path):
        ...


class CameraParamsRepository(Protocol):

    def get_cameras_param_list(self) -> list[IpCameraParam]:
        ...

    def get_camera_param_by_name(self, name: str) -> IpCameraParam:
        ...

    def get_camera_param_by_url(self, ip: str) -> IpCameraParam:
        ...


class ScalesParamsRepository(Protocol):

    def get_scales_param_list(self) -> list[ScalesParam]:
        ...

    def get_scales_param_by_name(self, name: str) -> ScalesParam:
        ...


class OrderRepository(Protocol):

    def get_orders(self) -> list[Order]:
        ...


class EquipmentsRepository(Protocol):

    def get_equipments(self) -> list[Equipment]:
        ...
