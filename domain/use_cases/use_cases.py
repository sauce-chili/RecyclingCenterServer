from domain.model.entities import *
from domain.repository import (
    CameraParamsRepository,
    ScalesParamsRepository,
    EquipmentsRepository,
    OrderRepository
)


class GetCameraNameListUseCase:

    def __init__(self, camera_repository: CameraParamsRepository):
        self.__cam_rep = camera_repository

    async def __call__(self) -> list[IpCameraParam]:
        return self.__cam_rep.get_cameras_param_list()


class GetScalesNameListUseCase:

    def __init__(self, scales_repository: ScalesParamsRepository):
        self.__scales_param_rep = scales_repository

    async def __call__(self) -> list[ScalesParam]:
        return self.__scales_param_rep.get_scales_param_list()


class GetEquipmentListUseCase:

    def __init__(self, equipment_repository: EquipmentsRepository):
        self.__equipment_rep = equipment_repository

    async def __call__(self) -> list[Equipment]:
        return self.__equipment_rep.get_equipments()


class GetOrdersListUseCase:

    def __init__(self, orders_repository: OrderRepository):
        self.__orders_repository = orders_repository

    async def __call__(self):
        return self.__orders_repository.get_orders()
