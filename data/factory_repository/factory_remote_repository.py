from pathlib import Path
from typing import Protocol

from data.repository_impl.remote_repository_impl import FtpRemoteRepository
from data.source.remote.server_ftp import ServerFTP, get_ftp_server_param, ParamFTP
from domain.repository import RemoteRepository
from domain.utils import get_database_param


class FactoryRemoteRepository(Protocol):

    def provide_remote_repository(self) -> RemoteRepository:
        ...


class FactoryFtpRemoteRepository(FactoryRemoteRepository):

    def __init__(self, yaml_cfg_path: Path):
        self.__cfg = yaml_cfg_path

    def provide_remote_repository(self) -> RemoteRepository:
        param_ftp: ParamFTP = get_ftp_server_param(self.__cfg)

        server: ServerFTP = ServerFTP(ftp_param=param_ftp)

        db_param = get_database_param(self.__cfg)

        return FtpRemoteRepository(
            server_ftp=server,
            db_param=db_param
        )
