from pathlib import Path

from domain.utils import get_arguments_from_yaml
from domain.repository import *


class YAMLCameraParamsRepository(CameraParamsRepository):
    __encoding: str = 'utf-8'
    __root_key: str = 'cameras_params'

    def __init__(self, path_to_yaml: Path):

        self.__cfg: dict | None = get_arguments_from_yaml(path_to_yaml_file=path_to_yaml, key=self.__root_key)

        self.__cameras_params: list[IpCameraParam] = [
            IpCameraParam(name=name, url=url) for url, name in self.__cfg.items()
        ]

        self.__correspondence_ip_to_cam_param = {
            cam_param.url: cam_param for cam_param in self.__cameras_params
        }

        self.__correspondence_name_to_cam_param = {
            cam_param.name: cam_param for cam_param in self.__cameras_params
        }

    def get_cameras_param_list(self) -> list[IpCameraParam]:
        return self.__cameras_params

    def get_camera_param_by_url(self, ip: str) -> IpCameraParam:

        if ip not in self.__correspondence_ip_to_cam_param:
            raise ValueError(f"""There are no parameters with this ip: {ip}""")

        return self.__correspondence_ip_to_cam_param[ip]

    def get_camera_param_by_name(self, name: str) -> IpCameraParam:

        if name not in self.__correspondence_name_to_cam_param:
            raise ValueError(f"""There are no parameters with this name: {name}""")

        return self.__correspondence_name_to_cam_param[name]

# path = Path('../device_configurations/CamerasParam.yaml')
# rep = YAMLCameraParamsRepository(path)
# print(rep.get_cameras_list())
