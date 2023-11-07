from pathlib import Path

from data.source.local.model import ApplicationStorageDto
from data.source.local.storage_waybills import StorageWaybills


class CSVWaybillsExporter:

    def __init__(self,
                 storage_waybills: StorageWaybills,
                 db_path: Path
                 ):
        self.__waybills_db: StorageWaybills = storage_waybills
        self.__db_path = db_path

    def __get_line_from_record(self, r: ApplicationStorageDto) -> str:
        return f'{r.id};{r.weighing_order};{r.source};{r.destination};{r.operation_type};\
        {r.camera_type};{r.scales_type};{r.weight_gross};{r.url_photo};{r.date}\n'

    def export(self) -> None:
        waybills: list[ApplicationStorageDto] = self.__waybills_db.get_all()

        with open(self.__db_path, mode='w', encoding='utf-8') as f:
            for application_dto in waybills:
                f.write(
                    self.__get_line_from_record(application_dto)
                )

# path_to_db = Path('C:\\Users\\dima6\\OneDrive\\Рабочий стол\\Testdb.db')
# dao_waybill = SQLiteStorageWaybill(db_path=path_to_db)
# path_to_out_csv_file = Path('C:\\Users\\dima6\\OneDrive\\Рабочий стол\\waybills.csv')
#
# csv_exporter = CSVWaybillsExporter(dao_waybill)
# csv_exporter.export(path_to_out_csv_file)
