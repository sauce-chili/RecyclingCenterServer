import yaml
from domain.repository import *
from pathlib import Path


class YAMLCameraParamsRepository(CameraParamsRepository):
    __encoding: str = 'utf-8'

    def __init__(self, path_to_yaml: Path):

        if not path_to_yaml.exists():
            raise FileExistsError(f"Camera config file {path_to_yaml} isn't exist.")

        self.__cfg: dict | None = None
        with open(path_to_yaml, encoding=self.__encoding, mode='r') as f:
            self.__cfg = yaml.load(f, Loader=yaml.Loader)

        self.__cameras_params: list[IpCameraParam] = [
            IpCameraParam(name=name, ip=ip) for ip, name in self.__cfg.items()
        ]

        self.__correspondence_ip_to_cam_param = {
            cam_param.ip: cam_param for cam_param in self.__cameras_params
        }

        self.__correspondence_name_to_cam_param = {
            cam_param.name: cam_param for cam_param in self.__cameras_params
        }

    def get_cameras_list(self) -> list[IpCameraParam]:
        return self.__cameras_params

    def get_camera_parameters_by_ip(self, ip: str) -> IpCameraParam:

        if ip not in self.__correspondence_ip_to_cam_param:
            raise ValueError(f"""There are no parameters with this ip: {ip}""")

        return self.__correspondence_ip_to_cam_param[ip]

    def get_camera_parameters_by_name(self, name: str) -> IpCameraParam:

        if name not in self.__correspondence_name_to_cam_param:
            raise ValueError(f"""There are no parameters with this name: {name}""")

        return self.__correspondence_name_to_cam_param[name]

# path = Path('device_configurations/CamerasParam.yaml')
# rep = YAMLCameraParamsRepository(path)
# print(rep.get_cameras_list())
