from threading import Lock
from pathlib import Path

import sqlite3

import queries
from data.source.local.model import SaveActiveApplicationDto, ActiveApplicationDto
from data.source.local.storage_active_applications import TemporaryStorageActiveApplications


class SQLiteTemporaryStorageActiveApplications(TemporaryStorageActiveApplications):
    __instance = None
    __lock = Lock()

    def __new__(cls, db_path: Path):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(SQLiteTemporaryStorageActiveApplications, cls).__new__(cls)
                    cls.__instance.__db_path = db_path
                    cls.__instance.__create_table_if_not_exists()
        return cls.__instance

    def __create_table_if_not_exists(self):
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(queries.query_create_application_table_if_not_exist)
        conn.commit()
        conn.close()

    def save(self, application_dto: SaveActiveApplicationDto) -> None:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()

        cursor.execute(
            queries.query_add_application_with_inc_weighing_order,
            (
                application_dto.source,
                application_dto.destination,
                application_dto.type_operation,
                application_dto.camera_type,
                application_dto.scales_type,
                application_dto.weight,
                application_dto.url_photo,
                application_dto.date
            )
        )

        conn.commit()
        conn.close()

    def get_all(self) -> list[ActiveApplicationDto]:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()

        cursor.execute(queries.query_get_all_application)
        records = cursor.fetchall()

        active_applications = [
            ActiveApplicationDto(
                weighing_order=weighing_order,
                source=source,
                destination=destination,
                type_operation=type_operation,
                camera_type=camera_type,
                scales_type=scales_type,
                weight=weight,
                url_photo=url_photo,
                date=date)
            for weighing_order, source, destination, type_operation, camera_type, scales_type, weight, url_photo, date
            in records
        ]

        conn.close()
        return active_applications

    def clear(self) -> None:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(queries.query_delete_all_applications)
        conn.commit()
        conn.close()

    def count_records(self) -> int:
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(queries.query_count_applications)
        count = cursor.fetchone()[0]
        conn.close()
        return count


# path_to_db = Path('C:\\Users\\dima6\\OneDrive\\Рабочий стол\\Testdb.db')
# temp_db = SQLiteTemporaryStorageActiveApplications(path_to_db)
#
# test_record = SaveActiveApplicationDto(
#     source="dsfsd",
#     destination="DROP TABLE active_application",
#     type_operation="intake",
#     camera_type="camera 1",
#     scales_type="scales 1",
#     weight=214.2,
#     url_photo="https://vk.com/im?sel=262646587",
#     date="18.10.2023"
# )
#
# temp_db.save(test_record)
# print(temp_db.get_all())
# print(temp_db.count_records())
# # temp_db.clear()
# print(temp_db.get_all())