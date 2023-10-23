from repository import LocalRepository, CameraParamsRepository, ScalesParamsRepository
from domain.controllers import CameraController, ScaleController
from domain.models import *


class SaveApplicationUseCase:

    def __init__(
            self,
            local_repository: LocalRepository,
            cameras_repository: CameraParamsRepository,
            scales_repository: ScalesParamsRepository,
            ip_cam_controller: CameraController,
            scales_controller: ScaleController
    ):
        self.__local_rep = local_repository
        self.__cam_rep = cameras_repository
        self.__scales_rep = scales_repository
        self.__ip_cam_controller = ip_cam_controller
        self.__scales_controller = scales_controller

    async def __call__(self, save_form: SaveApplicationForm):
        ...


class GetCameraNameListUseCase:

    def __init__(self, camera_repository: CameraParamsRepository):
        self.__cam_rep = camera_repository

    async def __call__(self) -> list[IpCameraParam]:
        return self.__cam_rep.get_cameras_list()


class GetScalesListUseCase:

    def __init__(self, scales_repository: ScalesParamsRepository):
        self.__scales_param_rep = scales_repository

    async def __call__(self) -> list[ScalesParam]:
        return self.__scales_param_rep.get_scales_list()
