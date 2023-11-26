import ftplib
import threading
from dataclasses import dataclass
from ftplib import FTP
from io import BytesIO
from pathlib import Path
from typing import Callable

from domain.utils import get_arguments_from_yaml


@dataclass
class ParamFTP:
    host: str
    username: str
    password: str


class ServerFTP:
    __instance = None

    def __new__(cls, ftp_param: ParamFTP):
        if cls.__instance is None:
            cls.__instance = super(ServerFTP, cls).__new__(cls)
            cls.__instance.__param_ftp = ftp_param
            cls.__instance.__connect()
        return cls.__instance

    def __connect(self):
        self.__ftp = FTP(self.__param_ftp.host)
        self.__ftp.login(user=self.__param_ftp.username, passwd=self.__param_ftp.password)
        self.__ftp.timeout = None

    def has_connection(self) -> bool:
        try:
            self.__ftp.voidcmd("NOOP")
            return True
        except (ConnectionError, ftplib.error_temp):
            return False

    def __root(self):
        with threading.Lock():
            if self.has_connection():
                self.__ftp.cwd('/')
            else:
                self.__connect()

    def __cwd(self, path_ftp: Path):
        try:
            if path_ftp.parent == self.__ftp.pwd():
                return

            for folder in path_ftp.parents:
                self.__ftp.cwd(folder.name)

        except Exception as e:
            self.__root()
            raise e

    def __execute_and_back_to_root(self, func: Callable, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            self.__root()

        return result

    def __execute_with_check_connection(self, func: Callable, *args, **kwargs):

        with threading.Lock():
            if not self.has_connection():
                self.__connect()

            func(*args, **kwargs)

    def file_exist(self, path_ftp_file: Path):

        try:
            self.__cwd(path_ftp_file)
        except:
            return False

        filed_in_folder = self.__ftp.nlst()

        self.__root()

        return path_ftp_file.name in filed_in_folder

    def __download_file(self, path_ftp_file: Path, path_local_file: Path):

        self.__cwd(path_ftp_file)

        with open(path_local_file, mode='wb') as local_file:
            self.__ftp.retrbinary('RETR ' + str(path_ftp_file.name), local_file.write)

    def download_file(self, path_ftp_file: Path, path_local_file: Path):

        self.__execute_and_back_to_root(
            lambda: self.__execute_with_check_connection(
                self.__download_file,
                path_ftp_file=path_ftp_file,
                path_local_file=path_local_file
            )
        )

    def __upload_file(self, path_local_file: Path, path_ftp_file: Path):

        self.__cwd(path_ftp_file)

        with open(path_local_file, mode='rb') as local_file:
            self.__ftp.storbinary('STOR ' + str(path_ftp_file.name), local_file)

    def upload_file(self, path_local_file: Path, path_ftp_file: Path):
        self.__execute_and_back_to_root(
            lambda: self.__execute_with_check_connection(
                self.__upload_file,
                path_local_file=path_local_file,
                path_ftp_file=path_ftp_file
            )
        )

    def __update_file(self, path_to_ftp_server: Path, source: BytesIO):
        self.__cwd(path_to_ftp_server)

        self.__ftp.storbinary(f'APPE {str(path_to_ftp_server.name)}', source, 1)

    def update_file(self, path_to_ftp_server: Path, source: BytesIO):
        self.__execute_and_back_to_root(
            lambda: self.__execute_with_check_connection(
                self.__update_file,
                path_to_ftp_server=path_to_ftp_server,
                source=source
            )
        )

    def get_url_to_file(self, ftp_file_path: str):
        if len(ftp_file_path) == 0:
            return ValueError("Path is empty.")

        return (f"ftp://{self.__param_ftp.username}@{self.__param_ftp.host}"
                f"/{ftp_file_path if ftp_file_path[0] != '/' else ftp_file_path[1:]}")


def get_ftp_server_param(yaml_param_ftp_server: Path):
    root_key = 'FTP_SERVER_PARAM'

    cfg = get_arguments_from_yaml(path_to_yaml_file=yaml_param_ftp_server, key=root_key)

    return ParamFTP(
        host=cfg['host'],
        username=cfg['username'],
        password=cfg['password']
    )

# p = get_ftp_server_param(Path('../../../configurations.yaml'))
# #
# server = ServerFTP(p)
#

# ftp_path = Path("for_tests/test.txt")
# server.upload_file(
#     path_ftp_file=ftp_path,
#     path_local_file=file
# )
#
# print(server.file_exist(ftp_path))
#
# buffer = BytesIO()
# buffer.write("test2\n".encode('utf-8'))
# buffer.seek(0)
#
#
# server.update_file(
#     path_to_ftp_server=ftp_path,
#     source=buffer
# )
#
# server.download_file(
#     path_ftp_file=ftp_path,
#     path_local_file=file
# )
