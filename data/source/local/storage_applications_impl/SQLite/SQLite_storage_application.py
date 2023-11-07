from threading import Lock
from pathlib import Path

import sqlite3

from . import queries
from data.source.local.model import PreservationApplicationDto, ApplicationStorageDto
from data.source.local.storage_applications import StorageApplications


class SQLiteStorageApplications(StorageApplications):

    def __init__(self, table_name: str, db_path: Path):
        self.__db_path = db_path
        self.__table_name = table_name
        self.__create_table_if_not_exists()

    def __create_table_if_not_exists(self):
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(queries.query_create_application_table_if_not_exist.format(table_name=self.__table_name))
        conn.commit()
        conn.close()

    def save(self, application_dto: PreservationApplicationDto) -> None:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()

        cursor.execute(
            queries.query_add_application.format(table_name=self.__table_name),
            (
                application_dto.car_plate,
                application_dto.counterparty,
                application_dto.operation_type,
                application_dto.equipment_type,
                application_dto.camera_type,
                application_dto.scales_type,
                application_dto.weight_gross,
                application_dto.weight_container,
                application_dto.weight_extra,
                application_dto.weight_net,
                application_dto.url_photo,
                application_dto.date,
                application_dto.end_weighing
            )
        )

        conn.commit()
        conn.close()

    def get_all(self) -> list[ApplicationStorageDto]:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()

        cursor.execute(queries.query_get_all_application.format(table_name=self.__table_name))
        records = cursor.fetchall()

        active_applications: list[ApplicationStorageDto] = [
            ApplicationStorageDto(*record) for record in records
        ]

        conn.close()
        return active_applications

    def remove_storage(self) -> None:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(queries.query_delete_table.format(table_name=self.__table_name))
        conn.commit()
        conn.close()

    def count_records(self) -> int:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(queries.query_count_applications.format(table_name=self.__table_name))
        count = cursor.fetchone()[0]
        conn.close()

        return count
