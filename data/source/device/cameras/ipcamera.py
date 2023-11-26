from pathlib import Path

import cv2


class IpCamera:

    def __init__(self, url_camera: str, path_storage_dir: Path):

        self.__check_path_to_storage_dir(path_storage_dir)

        self.__stor_dir = path_storage_dir

        self.__cap = cv2.VideoCapture(url_camera)

        if not self.__cap.isOpened():
            raise cv2.error(f'Unable to access the camera at the specified address {url_camera}')

        self.__cap.release()
        self.__url = url_camera

    def __check_path_to_storage_dir(self, path: Path) -> None:
        if not path.exists():
            raise FileExistsError(f'The specified photo storage path {path.absolute()} does not exist')
        elif not path.is_dir():
            raise FileExistsError(f'The the specified path {path.absolute()} must be a folder')

    def change_storage_dir(self, new_path_storage_dir: Path):

        self.__check_path_to_storage_dir(new_path_storage_dir)

        self.__stor_dir = new_path_storage_dir

    def take_photo(self, output_photo_name: str) -> Path:

        self.__cap = cv2.VideoCapture(self.__url)

        success, frame = self.__cap.read()

        if not success:
            raise cv2.error(f'Failed to read frame')

        full_path = self.__stor_dir / output_photo_name
        cv2.imwrite(str(full_path), frame)

        self.__cap.release()

        return full_path
