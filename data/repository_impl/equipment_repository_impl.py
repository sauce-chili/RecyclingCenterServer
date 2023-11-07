from pathlib import Path
from dataclasses import dataclass

from domain.repository import EquipmentsRepository
from domain.models import Equipment
from data.source.remote.server_ftp import ServerFTP
from domain.utils import get_arguments_from_yaml


@dataclass
class ParamFtpEquipmentRepository:
    ftp_equipment_path: Path
    local_equipment_buffer_path: Path


class FtpEquipmentRepository(EquipmentsRepository):
    __encoding = 'utf-8'

    def __init__(
            self,
            ftp_server: ServerFTP,
            paths: ParamFtpEquipmentRepository
    ):
        self.__server = ftp_server
        self.__buffer_file = paths.local_equipment_buffer_path
        self.__ftp_path_equipment_path = paths.ftp_equipment_path

    def get_equipments(self) -> list[Equipment]:
        self.__server.download_file(
            path_ftp_file=self.__ftp_path_equipment_path,
            path_local_file=self.__buffer_file
        )

        equipment_result: list[Equipment] = []

        with open(file=self.__buffer_file, encoding=self.__encoding, mode='r+') as f:
            for equipment_name in f:
                if equipment_name == '\n': continue

                equipment_result.append(Equipment(name=equipment_name.strip('\\n\n')))

            f.truncate()

        return equipment_result


def get_ParamFtpEquipmentRepository(yaml_config_path: Path) -> ParamFtpEquipmentRepository:
    root_key = 'FTP_EQUIPMENTS_REPOSITORY_PARAM'

    cfg = get_arguments_from_yaml(path_to_yaml_file=yaml_config_path, key=root_key)

    return ParamFtpEquipmentRepository(
        ftp_equipment_path=Path(cfg['ftp_equipments_path']),
        local_equipment_buffer_path=Path(cfg['local_equipments_buffer_path'])
    )

# print(get_ParamFtpEquipmentRepository(Path('../../app/configurations.yaml')))
