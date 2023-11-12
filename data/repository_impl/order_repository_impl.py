from dataclasses import dataclass
from pathlib import Path

from data.source.remote.server_ftp import ServerFTP
from domain.model.entities import Order
from domain.repository import OrderRepository
from domain.utils import get_arguments_from_yaml


@dataclass
class ParamFtpOrderRepository:
    ftp_path_to_orders: Path
    local_orders_buffer_path: Path


class FtpOrderRepository(OrderRepository):
    __encoding = 'utf-8'
    __separator = ','

    def __init__(self,
                 ftp_server: ServerFTP,
                 paths: ParamFtpOrderRepository):
        self.__server = ftp_server
        self.__buffer_file = paths.local_orders_buffer_path
        self.__ftp_path_orders = paths.ftp_path_to_orders

    def get_orders(self) -> list[Order]:

        self.__server.download_file(
            path_ftp_file=self.__ftp_path_orders,
            path_local_file=self.__buffer_file
        )

        orders: dict[str, set[str]] = dict()

        with open(file=self.__buffer_file, mode='r+', encoding=self.__encoding) as f:

            for record in f:
                if record == '\n': continue

                # skip iin column
                counterparty, _, car_plate = record.strip('\\n\r\n').split(self.__separator)

                if counterparty not in orders:
                    orders[counterparty] = set()

                orders[counterparty].add(car_plate)

            f.truncate()

        orders_result: list[Order] = [
            Order(counterparty=k, car_plates=v)
            for k, v in orders.items()
        ]

        return orders_result


def get_ParamFtpOrderRepository(yaml_config_path: Path) -> ParamFtpOrderRepository:
    root_key = 'FTP_ORDER_REPOSITORY_PARAM'

    cfg: list[dict] | None = get_arguments_from_yaml(path_to_yaml_file=yaml_config_path, key=root_key)

    return ParamFtpOrderRepository(
        ftp_path_to_orders=Path(cfg['ftp_order_path']),
        local_orders_buffer_path=Path(cfg['local_order_buffer_path'])
    )

# print(get_FtpOrderRepository_param(Path('../../app/configurations.yaml')))
