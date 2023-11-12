from pathlib import Path

from domain.repository import *
from domain.utils import get_arguments_from_yaml


class YAMLScalesParamsRepository(ScalesParamsRepository):
    __nameOrig: str = "nameOriginal"
    __nameRu: str = "nameRu"
    __port: str = "port"

    __root_key: str = 'scales_params'
    __encoding: str = 'utf-8'

    def __init__(self, path_to_yaml: Path):
        self.__cfg = get_arguments_from_yaml(path_to_yaml_file=path_to_yaml, key=self.__root_key)

        self.__scales_param: list[ScalesParam] = [
            ScalesParam(
                nameOrigin=param[self.__nameOrig],
                nameRu=param[self.__nameRu],
                port=param[self.__port]
            )
            for param in self.__cfg
        ]

    def get_scales_param_list(self) -> list[ScalesParam]:
        return self.__scales_param

    def get_scales_param_by_name(self, name: str) -> ScalesParam:
        matched = [param for param in self.__scales_param
                   if name == param.nameOrigin or name == param.nameRu]

        if len(matched) == 0:
            raise ValueError(f"""There are no parameters with this name: {name}.""")

        return matched[0]


# scales_path_cfg_path = Path('../device_configurations/ScalesParam.yaml')
# scales_rep = YAMLScalesParamsRepository(scales_path_cfg_path)
# print(scales_rep.get_scales_list())
# print(scales_rep.get_scales_by_name('Весы 1'))
