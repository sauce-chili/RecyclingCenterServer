from pathlib import Path
from typing import Protocol

from data.repository_impl.application_repository_impl import RemoteCSVApplicationRepository
from data.source.remote.server_ftp import ServerFTP, ParamFTP, get_ftp_server_param
from domain.model.entities import DatabaseParam
from domain.repository import ApplicationRepository
from domain.utils import get_database_param


class FactoryApplicationsRepository(Protocol):

    def provide_application_repository(self) -> ApplicationRepository:
        ...


class FactoryRemoteCSVApplicationRepository(FactoryApplicationsRepository):

    def __init__(self, yaml_cfg_path: Path, ):
        self.__cfg = yaml_cfg_path

    def provide_application_repository(self) -> ApplicationRepository:
        param_ftp: ParamFTP = get_ftp_server_param(self.__cfg)

        server: ServerFTP = ServerFTP(ftp_param=param_ftp)

        db_param: DatabaseParam = get_database_param(self.__cfg)

        return RemoteCSVApplicationRepository(
            db_param=db_param,
            server_ftp=server
        )
