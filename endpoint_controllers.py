from domain.model.entities import *
from domain.model.request_schema import *
from domain.model.response_schema import *
from domain.use_cases.factory_usecases.factory_save_application_of_end_weighting_use_case import FactorySaveApplicationOfEndWeightingUseCase
from domain.use_cases.factory_usecases.factory_save_application_use_case import FactorySaveApplicationUseCase
from domain.use_cases.factory_usecases.factory_get_equipment_list_use_case import FactoryGetEquipmentListUseCase
from domain.use_cases.factory_usecases.factory_get_orders_list_use_case import FactoryGetOrdersListUseCase
from domain.use_cases.factory_usecases.factory_get_scales_name_use_case import FactoryGetScalesNameListUseCase
from domain.use_cases.use_cases import GetEquipmentListUseCase
from domain.use_cases.use_cases import GetOrdersListUseCase
from domain.use_cases.use_cases import GetScalesNameListUseCase
from domain.use_cases.save_application_use_case import SaveApplicationUseCase
from domain.use_cases.save_application_of_end_weighting import SaveApplicationOfEndWeightingUseCase



class MainControllerV1:

    def __init__(self, cfg_file: Path):
        self.__save_app_usecase: SaveApplicationUseCase = FactorySaveApplicationUseCase(
            yaml_cfg_file=cfg_file
        ).provide()
        
        self.__end_weighting_usecase: SaveApplicationOfEndWeightingUseCase = FactorySaveApplicationOfEndWeightingUseCase(
            yaml_cfg_file=cfg_file
        ).provide()

        self.__get_scales_type_usecase: GetScalesNameListUseCase = FactoryGetScalesNameListUseCase(
            yaml_cfg_file=cfg_file
        ).provide()

        self.__get_orders_usecase: GetOrdersListUseCase = FactoryGetOrdersListUseCase(
            yaml_cfg_file=cfg_file
        ).provide()

        self.__get_equipment_usecase: GetEquipmentListUseCase = FactoryGetEquipmentListUseCase(
            yaml_cfg_file=cfg_file
        ).provide()

    async def save_application(self, save_application_request: SaveApplicationRequest):
        result_save: ResultSaveApplication = await self.__save_app_usecase(save_request=save_application_request)

        return SaveApplicationResponse(
            weight_gross=result_save.weight_gross,
            weight_net=result_save.weight_net,
            url_photo=result_save.url_photo
        )

    async def save_application_of_end_weighting(
            self,
            save_application_of_end_weighting_request: SaveApplicationOfEndWeightingRequest
    ):
        await self.__end_weighting_usecase(
            end_weighting_request=save_application_of_end_weighting_request
        )

    async def get_scales_names(self):
        scalesType = await self.__get_scales_type_usecase()

        return [ScalesTypeResponse(
            nameEng=param.nameOrigin,
            nameRu=param.nameRu
        )
            for param in scalesType
        ]

    async def get_orders_list(self):
        orders = await self.__get_orders_usecase()

        response_orders = [
            OrderResponse(counterparty=o.counterparty, car_plates=list(o.car_plates))
            for o in orders
        ]

        return response_orders

    async def get_equipments_list(self):
        equipment = await self.__get_equipment_usecase()

        return [EquipmentResponse(name=e.name) for e in equipment]
