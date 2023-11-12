import os
import secrets
import string
from datetime import datetime
from pathlib import Path

from data.source.local.model import ApplicationStorageDto
from data.source.local.utils import storage_dto_to_csv_line
from data.source.remote.server_ftp import ServerFTP
from domain.model.entities import ApplicationForm, DatabaseParam, ResultSaveApplication
from domain.repository import ApplicationRepository, ClosingApplication


def _get_strtime_format(data: datetime) -> str:
    return data.strftime("%d-%m-%Y-%H-%M-%S")


def _get_closing_applications(id: str, form: ClosingApplication) -> ApplicationStorageDto:
    return ApplicationStorageDto(
        id=id,
        car_plate=form.car_plate,
        counterparty=form.counterparty,
        operation_type=form.operation_type,
        equipment_type=form.equipment_type,
        camera_type=None,
        scales_type=None,
        weight_gross=None,
        weight_extra=None,
        weight_net=None,
        weight_container=None,
        url_photo=None,
        date=_get_strtime_format(form.date),
        end_weighing=1
    )


class RemoteCSVApplicationRepository(ApplicationRepository):
    __separator = '|'
    __length_id = 9
    __alphabet_of_id = string.digits

    __instance = None

    def __new__(cls, db_param: DatabaseParam, server_ftp: ServerFTP):

        if cls.__instance is not None:
            return cls.__instance

        cls.__instance = super(RemoteCSVApplicationRepository, cls).__new__(cls)
        cls.__instance.__ftp_server = server_ftp
        cls.__instance.__db_param = db_param

    def __generate_id(self) -> str:
        uuid = ''.join(secrets.choice(self.__alphabet_of_id) for _ in range(self.__length_id))
        return uuid

    def __get_application_storage_dto(
            self,
            app_form: ApplicationForm,
            id: str,
            ftp_url_photo: str = None
    ) -> ApplicationStorageDto:
        return ApplicationStorageDto(
            id=id,
            counterparty=app_form.counterparty,
            car_plate=app_form.car_plate,
            operation_type=app_form.operation_type,
            equipment_type=app_form.operation_type,
            camera_type=app_form.camera_type,
            scales_type=app_form.scales_type,
            weight_gross=app_form.weight_gross,
            weight_extra=app_form.weight_extra,
            weight_container=app_form.weight_container,
            weight_net=app_form.weight_net,
            url_photo=ftp_url_photo,
            date=_get_strtime_format(app_form.date),
            end_weighing=0
        )

    def __remove_photo_from_buffer(self, path_to_path: Path):
        if path_to_path.exists() and path_to_path.is_file():
            os.remove(path_to_path)

    def __add_record(self, new_csv_record: str):
        if self.__ftp_server.file_exist(path_ftp_file=self.__db_param.db_remote_path):
            self.__ftp_server.download_file(
                path_ftp_file=self.__db_param.db_remote_path,
                path_local_file=self.__db_param.db_path
            )

        with open(self.__db_param.db_path, mode='a') as f:
            f.write(new_csv_record)

        self.__ftp_server.upload_file(
            path_ftp_file=self.__db_param.db_remote_path,
            path_local_file=self.__db_param.db_path
        )

    def save_application(self, application_form: ApplicationForm) -> ResultSaveApplication:
        Id = self.__generate_id()

        photo_ftp_name = f'{Id}_{_get_strtime_format(application_form.date)}.png'

        photo_ftp_path = self.__db_param.image_buffer_folder_remote_path / photo_ftp_name

        self.__ftp_server.upload_file(
            path_local_file=application_form.local_path_photo,
            path_ftp_file=photo_ftp_path
        )

        self.__remove_photo_from_buffer(application_form.local_path_photo)

        url_ftp_photo = self.__ftp_server.get_url_to_file(str(photo_ftp_path))

        dto: ApplicationStorageDto = self.__get_application_storage_dto(
            id=Id,
            ftp_url_photo=url_ftp_photo,
            app_form=application_form
        )

        csv_line = storage_dto_to_csv_line(
            dto=dto,
            separator=self.__separator
        )

        self.__add_record(new_csv_record=csv_line)

        return ResultSaveApplication(
            weight_net=application_form.weight_net,
            weight_gross=application_form.weight_gross,
            url_photo=url_ftp_photo
        )

    def close_application(self, closing_application_from: ClosingApplication) -> None:
        Id: str = self.__generate_id()

        dto: ApplicationStorageDto = _get_closing_applications(
            id=Id,
            form=closing_application_from
        )

        csv_line = storage_dto_to_csv_line(
            dto=dto,
        )

        self.__add_record(new_csv_record=csv_line)
