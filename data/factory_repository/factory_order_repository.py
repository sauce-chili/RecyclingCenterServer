from pathlib import Path

from domain.repository import OrderRepository
from typing import Protocol

from data.source.remote.server_ftp import (
    ServerFTP,
    ParamFTP,
    get_ftp_server_param
)
from data.repository_impl.order_repository_impl import (
    FtpOrderRepository,
    ParamFtpOrderRepository,
    get_ParamFtpOrderRepository
)


class FactoryOrderRepository(Protocol):

    def provide_order_repository(self) -> OrderRepository:
        ...


class FactoryFtpOrderRepository(FactoryOrderRepository):

    def __init__(self, param_cfg_file_path: Path):
        self.__cfg = param_cfg_file_path

    def provide_order_repository(self) -> OrderRepository:
        param_ftp_server: ParamFTP = get_ftp_server_param(self.__cfg)
        # print(param_ftp_server)
        ftp_server = ServerFTP(ftp_param=param_ftp_server)

        param_ftp_order_repository: ParamFtpOrderRepository = get_ParamFtpOrderRepository(self.__cfg)
        # print(param_order_repository)

        return FtpOrderRepository(
            ftp_server=ftp_server,
            paths=param_ftp_order_repository
        )

# print(FactoryFtpOrderRepository(Path('../../app/configurations.yaml')).provide_order_repository())
