from pathlib import Path

from data.factory_repository.factory_application_repository import FactoryRemoteCSVApplicationRepository
from domain.repository import ApplicationRepository
from domain.use_cases.save_application_of_end_weighting import SaveApplicationOfEndWeightingUseCase


class FactorySaveApplicationOfEndWeightingUseCase:

    def __init__(self, yaml_cfg_file: Path):
        if not yaml_cfg_file.exists():
            raise FileExistsError(f"Config file {yaml_cfg_file} doesn't exist")

        self.__cfg = yaml_cfg_file

    def provide(self):
        app_rep: ApplicationRepository = FactoryRemoteCSVApplicationRepository(
            yaml_cfg_path=self.__cfg
        ).provide_application_repository()

        return SaveApplicationOfEndWeightingUseCase(
            application_repository=app_rep
        )
