import yaml
from domain.repository import *
from pathlib import Path


class YAMLScalesParamsRepository(ScalesParamsRepository):

    class __YamlParam:
        nameOrig: str = "nameOriginal"
        nameRu: str = "nameRu"
        port: str = "port"


    __encoding: str = 'utf-8'

    def __init__(self, path_to_yaml: Path):
        if not path_to_yaml.exists():
            raise FileExistsError(f"Scales config file {path_to_yaml} isn't exist.")

        self.__cfg: list[dict] | None = None
        with open(path_to_yaml, encoding=self.__encoding, mode='r') as f:
            self.__cfg = yaml.load(f, Loader=yaml.Loader)
            print(self.__cfg)

        self.__scales_param: list[ScalesParam] = [
            ScalesParam(
                nameOrigin=param[self.__YamlParam.nameOrig],
                nameRu=param[self.__YamlParam.nameRu],
                port=param[self.__YamlParam.port]
            )
            for param in self.__cfg
        ]

    def get_scales_list(self) -> list[ScalesParam]:
        return self.__scales_param

    def get_scales_by_name(self, name: str) -> ScalesParam:

        matched = [param for param in self.__scales_param
                   if name == param.nameOrigin or name == param.nameRu]

        if len(matched) == 0:
            raise ValueError(f"""There are no parameters with this name: {name}.""")

        return matched[0]

# scales_path_cfg_path = Path('device_configurations/ScalesParam.yaml')
# scales_rep = YAMLScalesParamsRepository(scales_path_cfg_path)
# print(scales_rep.get_scales_list())
# print(scales_rep.get_scales_by_name('Весы 1'))
