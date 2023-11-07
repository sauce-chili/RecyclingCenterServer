from typing import Protocol
from pathlib import Path

from domain.repository import EquipmentsRepository
from data.repository_impl.equipment_repository_impl import (
    FtpEquipmentRepository,
    ParamFtpEquipmentRepository,
    get_ParamFtpEquipmentRepository
)
from data.source.remote.server_ftp import (
    ServerFTP,
    ParamFTP,
    get_ftp_server_param
)


class FactoryEquipmentsRepository(Protocol):

    def provide_equipments_repository(self) -> EquipmentsRepository:
        ...


class FactoryFtpEquipmentsRepository(FactoryEquipmentsRepository):

    def __init__(self, param_cfg_file_path: Path):
        self.__cfg = param_cfg_file_path

    def provide_equipments_repository(self) -> EquipmentsRepository:
        param_ftp_server: ParamFTP = get_ftp_server_param(self.__cfg)
        server_ftp = ServerFTP(ftp_param=param_ftp_server)

        param_ftp_equipments_repository: ParamFtpEquipmentRepository = get_ParamFtpEquipmentRepository(
            yaml_config_path=self.__cfg
        )

        return FtpEquipmentRepository(
            ftp_server=server_ftp,
            paths=param_ftp_equipments_repository
        )
