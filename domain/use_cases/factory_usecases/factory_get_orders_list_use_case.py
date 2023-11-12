from pathlib import Path

from data.factory_repository.factory_order_repository import FactoryFtpOrderRepository
from domain.repository import OrderRepository
from domain.use_cases.use_cases import GetOrdersListUseCase


class FactoryGetOrdersListUseCase:

    def __init__(self, yaml_cfg_file: Path):
        if not yaml_cfg_file.exists():
            raise FileExistsError(f"Config file {yaml_cfg_file} doesn't exist")

        self.__cfg = yaml_cfg_file

    def provide(self) -> GetOrdersListUseCase:
        orders_rep: OrderRepository = FactoryFtpOrderRepository(
            param_cfg_file_path=self.__cfg
        ).provide_order_repository()

        return GetOrdersListUseCase(
            orders_repository=orders_rep
        )
