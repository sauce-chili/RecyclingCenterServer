from pathlib import Path

from domain.utils import get_database_param
from data.source.local.table_names import APPLICATION_TABLE_NAME
from data.source.local.storage_applications import StorageApplications
from data.source.local.storage_applications_impl.SQLite.SQLite_storage_application import SQLiteStorageApplications
from typing import Protocol


class FactoryStorageApplication(Protocol):

    def provide_storage_application(self) -> StorageApplications:
        ...


class FactorySQLiteStorageApplication(FactoryStorageApplication):

    def __init__(self, yaml_cfg_path: Path):
        self.__cfg = yaml_cfg_path

    def provide_storage_application(self) -> StorageApplications:
        param_db = get_database_param(self.__cfg)

        return SQLiteStorageApplications(
            db_path=param_db.db_path,
            table_name=APPLICATION_TABLE_NAME
        )
