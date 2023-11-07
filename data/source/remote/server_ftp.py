from dataclasses import dataclass
from ftplib import FTP
from pathlib import Path

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
            cls.__instance.__ftp = FTP(ftp_param.host)
            cls.__instance.__ftp.login(user=ftp_param.username, passwd=ftp_param.password)
            cls.__instance.__param_ftp = ftp_param
        return cls.__instance

    def download_file(self, path_ftp_file: Path, path_local_file: Path):

        for folder in path_ftp_file.parents:
            self.__ftp.cwd(folder.name)

        with open(path_local_file, mode='wb') as local_file:
            self.__ftp.retrbinary('RETR ' + str(path_ftp_file.name), local_file.write)

    def upload_file(self, path_local_file: Path, path_ftp_file: Path):

        for folder in path_ftp_file.parents:
            self.__ftp.cwd(folder.name)

        with open(path_local_file, mode='rb') as local_file:
            self.__ftp.storbinary('STOR ' + str(path_ftp_file.name), local_file)

    def get_url_to_file(self, ftp_file_path: str):
        return f"ftp://{self.__param_ftp.username}@{self.__param_ftp.host}/{ftp_file_path}"

    def __del__(self):
        self.__ftp.quit()


def get_ftp_server_param(yaml_param_ftp_server: Path):
    root_key = 'FTP_SERVER_PARAM'

    cfg = get_arguments_from_yaml(path_to_yaml_file=yaml_param_ftp_server, key=root_key)

    return ParamFTP(
        host=cfg['host'],
        username=cfg['username'],
        password=cfg['password']
    )

# p = get_ftp_server_param(Path('../../../app/configurations.yaml'))
#
# server = ServerFTP(p)
#
# file = Path('D:\\programms\\Python\\RecyclingCenterServer\\db\\buffer_images\\test1.png')
#
# server.upload_file(
#     path_ftp_file=Path(f"/images/{file.name}"),
#     path_local_file=file
# )
