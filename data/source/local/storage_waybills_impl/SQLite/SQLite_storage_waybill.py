from threading import Lock
from pathlib import Path

import sqlite3

from data.source.local.model import ApplicationDto
from data.source.local.storage_waybills import StorageWaybills

from . import queries


class SQLiteStorageWaybill(StorageWaybills):
    __instance = None
    __lock = Lock()

    def __new__(cls, db_path: Path):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(SQLiteStorageWaybill, cls).__new__(cls)
                    cls.__instance.__db_path = db_path
                    cls.__instance.__create_table_if_not_exists()
        return cls.__instance

    def __create_table_if_not_exists(self):
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(queries.query_create_table_waybill_if_not_exist)
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(queries.query_insert_all_records_from_active_application_table)
        conn.commit()
        conn.close()

    def get_all(self) -> list[ApplicationDto]:

        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()

        cursor.execute(queries.query_get_all)
        records = cursor.fetchall()

        active_applications = [
            ApplicationDto(
                id=id,
                weighing_order=weighing_order,
                source=source,
                destination=destination,
                type_operation=type_operation,
                camera_type=camera_type,
                scales_type=scales_type,
                weight=weight,
                url_photo=url_photo,
                date=date)
            for
            id, weighing_order, source, destination, type_operation, camera_type, scales_type, weight, url_photo, date
            in records
        ]

        conn.close()

        return active_applications


# path_to_db = Path('C:\\Users\\dima6\\OneDrive\\Рабочий стол\\Testdb.db')
# dao_waybill = SQLiteStorageWaybill(db_path=path_to_db)
# records = dao_waybill.get_all()
# print(f'records:\n{records}\n number of records: {len(records)}')
# dao_waybill.save()
# records = dao_waybill.get_all()
# print(f'records:\n{records}\n number of records: {len(records)}')