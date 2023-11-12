from pathlib import Path

from data.repository_impl.scales_params_repository_impl import YAMLScalesParamsRepository
from domain.use_cases.use_cases import GetScalesNameListUseCase


class FactoryGetScalesNameListUseCase:

    def __init__(self, yaml_cfg_file: Path):
        if not yaml_cfg_file.exists():
            raise FileExistsError(f"Config file {yaml_cfg_file} doesn't exist")

        self.__cfg = yaml_cfg_file

    def provide(self) -> GetScalesNameListUseCase:
        scales_rep = YAMLScalesParamsRepository(
            path_to_yaml=self.__cfg
        )

        return GetScalesNameListUseCase(
            scales_repository=scales_rep
        )
