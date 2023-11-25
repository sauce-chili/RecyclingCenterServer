from data.source.device.cameras.ipcamera import IpCamera
from domain.controllers import *
from domain.exeptions import *
from pathlib import Path


class IPCameraController(CameraController):

    def __init__(self, path_storage_dir: Path, cameras_param: list[IpCameraParam]):
        if not path_storage_dir.exists() or not path_storage_dir.is_dir():
            raise FileExistsError(f'The specified photo storage path {path_storage_dir.absolute()} does not exist')

        self.__storage_dir: Path = path_storage_dir

        self.__ip_cams: dict[IpCameraParam, IpCamera] = {
            cam_param: IpCamera(url_camera=cam_param.url, path_storage_dir=path_storage_dir)
            for cam_param in cameras_param
        }

    def take_photo(self, output_file_name: str, camera: IpCameraParam) -> Path:

        if camera not in self.__ip_cams:
            raise CameraNotAvailableException("There is no known camera with these parameters")

        # The camera stream may be busy, so we try to access it several times, before throwing an exception
        for _ in range(5):
            try:
                path_to_saved_photo = self.__ip_cams[camera].take_photo(output_file_name)
                return path_to_saved_photo
            except Exception as e:
                pass

        raise CameraNotAvailableException("Unable to access camera, check connection")
