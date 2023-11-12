from pathlib import Path

from data.factory_repository.factory_equipment_repository import FactoryFtpEquipmentsRepository
from domain.repository import EquipmentsRepository
from domain.use_cases.use_cases import GetEquipmentListUseCase


class FactoryGetEquipmentListUseCase:

    def __init__(self, yaml_cfg_file: Path):
        if not yaml_cfg_file.exists():
            raise FileExistsError(f"Config file {yaml_cfg_file} doesn't exist")

        self.__cfg = yaml_cfg_file

    def provide(self) -> GetEquipmentListUseCase:
        equipment_rep: EquipmentsRepository = FactoryFtpEquipmentsRepository(
            param_cfg_file_path=self.__cfg
        ).provide_equipments_repository()

        return GetEquipmentListUseCase(
            equipment_repository=equipment_rep
        )
