from dataclasses import dataclass
from ftplib import FTP, error_temp
from pathlib import Path
from typing import Callable

# from ftputil import FTPHost

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

    def __root(self):
        try:
            self.__ftp.cwd('/')
        except BrokenPipeError as pipe_error:
            # try reconnect
            self.__connect()
            self.__ftp.cwd('/')
        except EOFError:
            self.__connect()
            self.__ftp.cwd('/')
        except Exception as e:
            print(e)
            print(type(e))

    def __cwd(self, path_ftp: Path):
        try:
            # problem area, an incomprehensible error often pops up
            # if path_ftp.parent == self.__ftp.pwd():
            #     return
    
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
        # try:
        #     self.__cwd(path_ftp_file)
        #
        #     with open(path_local_file, mode='wb') as local_file:
        #         self.__ftp.retrbinary('RETR ' + str(path_ftp_file.name), local_file.write)
        # except Exception as e:
        #     self.__root()
        #     raise e

        self.__execute_and_back_to_root(
            self.__download_file,
            path_ftp_file=path_ftp_file,
            path_local_file=path_local_file
        )

    def __upload_file(self, path_local_file: Path, path_ftp_file: Path):
        self.__cwd(path_ftp_file)
        
        with open(path_local_file, mode='rb') as local_file:
            self.__ftp.storbinary('STOR ' + str(path_ftp_file.name), local_file)

    def upload_file(self, path_local_file: Path, path_ftp_file: Path):
        # try:
        #     self.__cwd(path_ftp_file)
        #
        #     with open(path_local_file, mode='rb') as local_file:
        #         self.__ftp.storbinary('STOR ' + str(path_ftp_file.name), local_file)
        # except Exception as e:
        #     self.__root()
        #     raise e

        self.__execute_and_back_to_root(
            self.__upload_file,
            path_local_file=path_local_file,
            path_ftp_file=path_ftp_file
        )

    def get_url_to_file(self, ftp_file_path: str):
        return f"ftp://{self.__param_ftp.username}@{self.__param_ftp.host}/{ftp_file_path}"


# Version with cache
# class ServerFTP_V2:
#     __instance = None

#     def __new__(cls, ftp_param: ParamFTP):
#         if cls.__instance is None:
#             cls.__instance = super(ServerFTP_V2, cls).__new__(cls)

#             ftp_host = FTPHost(
#                 ftp_param.host,
#                 ftp_param.username,
#                 ftp_param.password
#             )

#             ftp_host.stat_cache.max_age = 60 * 60  # one hour

#             cls.__instance.__ftp_host = ftp_host
#             cls.__instance.__param_ftp = ftp_param
#         return cls.__instance

#     def __root(self):
#         self.__ftp_host.chdir('/')

#     def __execute_and_back_to_root(self, func: Callable, *args, **kwargs):
#         try:
#             result = func(*args, **kwargs)
#         except Exception as e:
#             raise e
#         finally:
#             self.__root()

#         return result

#     def __cwd(self, path_ftp):
#         try:
#             if path_ftp.parent == self.__ftp_host.getcwd():
#                 return

#             for folder in path_ftp.parents:
#                 self.__ftp_host.chdir(folder.name)
#         except Exception as e:
#             self.__root()
#             raise e

#     def __file_exists(self, path_ftp_file: Path) -> bool:
#         try:
#             self.__cwd(path_ftp_file)
#         except:
#             return False

#         return self.__ftp_host.path.exists(path_ftp_file.name)

#     def file_exist(self, path_ftp_file):
#         return self.__execute_and_back_to_root(
#             self.__file_exists,
#             path_ftp_file=path_ftp_file
#         )

#     def download_file(self, path_ftp_file: Path, path_local_file: Path):

#         self.__cwd(path_ftp_file)

#         self.__execute_and_back_to_root(
#             self.__ftp_host.download_if_newer,
#             source=str(path_ftp_file.name),
#             target=str(path_local_file)
#         )

#     def upload_file(self, path_local_file: Path, path_ftp_file: Path):

#         self.__cwd(path_ftp_file)

#         self.__execute_and_back_to_root(
#             self.__ftp_host.upload_if_newer,
#             source=str(path_local_file),
#             target=str(path_ftp_file.name)
#         )


def get_ftp_server_param(yaml_param_ftp_server: Path):
    root_key = 'FTP_SERVER_PARAM'

    cfg = get_arguments_from_yaml(path_to_yaml_file=yaml_param_ftp_server, key=root_key)

    return ParamFTP(
        host=cfg['host'],
        username=cfg['username'],
        password=cfg['password']
    )

# p = get_ftp_server_param(Path('../../../app/configurations.yaml'))
# #
# server = ServerFTP_V2(p)
#
# file = Path('D:\\programms\\Python\\RecyclingCenterServer\\db\\buffer_images\\inbound_Pfdiu.png')

# server.upload_file(
#     path_ftp_file=Path(f"images/{file.name}"),
#     path_local_file=file
# )

# print(server.file_exist(Path('/images/inbound_Pfdiu.png')))

# server.download_file(
#     path_ftp_file=Path(f"/images/inbound_Pfdiu.png"),
#     path_local_file=Path(f"D:\\programms\\Python\\RecyclingCenterServer\\db\\buffer_images\\inbound_Pfdiu.png")
# )

# server.update_file(
#     path_ftp_file=Path('performed_order.csv'),
#     source_buffer=StringIO("test1")
# )
# server.update_file(
#     path_ftp_file=Path('performed_order.csv'),
#     source_buffer=StringIO("test2")
# )
