import secrets
import string
from pathlib import Path
from datetime import datetime
import os

from domain.repository import (
    ApplicationRepository,
    RemoteRepository,
    CameraParamsRepository,
    ScalesParamsRepository,
)
from domain.controllers import CameraController, ScaleController
from domain.models import (
    PreservationApplicationForm,
    IpCameraParam, ApplicationForm,
    ScalesParam,
    ResultSaveApplication
)


class SaveApplicationUseCase:

    def __generate_uuid(self, length: int) -> str:
        alphabet = string.ascii_letters + string.digits
        print(len(alphabet))
        uuid = ''.join(secrets.choice(alphabet) for _ in range(length))
        return uuid

    def __remove_photo_from_buffer(self, path_to_path: Path):
        if path_to_path.exists() and path_to_path.is_file():
            os.remove(path_to_path)

    def __get_net_weight(self, gross_w: float, container_w: float, extra_w: float):
        return gross_w - container_w - gross_w * extra_w

    def __init__(
            self,
            local_repository: ApplicationRepository,
            remote_repository: RemoteRepository,
            cameras_repository: CameraParamsRepository,
            scales_repository: ScalesParamsRepository,
            ip_cam_controller: CameraController,
            scales_controller: ScaleController
    ):
        self.__local_rep = local_repository
        self._remote_rep = remote_repository
        self.__cam_rep = cameras_repository
        self.__scales_rep = scales_repository
        self.__ip_cam_controller = ip_cam_controller
        self.__scales_controller = scales_controller

    async def __call__(self, save_form: PreservationApplicationForm) -> ResultSaveApplication:
        scales_param: ScalesParam = self.__scales_rep.get_scales_param_by_name(save_form.scales_type)
        gross_weight: float = self.__scales_controller.weight(scales_param).result

        net_weight: float = self.__get_net_weight(
            gross_w=gross_weight,
            container_w=save_form.weight_container,
            extra_w=save_form.weight_extra
        )

        cam_name: str | None = save_form.camera_type

        cam_param: IpCameraParam

        '''
        In the first version of the project there were supposed to be 2 cameras types, 
        but then the decision was made to mount only one, so the `camera_type` field is passing empty
        '''
        if cam_name is None:
            cam_param = self.__cam_rep.get_cameras_param_list()[0]
        else:
            cam_param: IpCameraParam = self.__cam_rep.get_camera_param_by_name(cam_name)

        name_of_photo: str = f'{save_form.operation_type}_{self.__generate_uuid(length=5)}'
        path_to_photo = self.__ip_cam_controller.take_photo(
            output_file_name=name_of_photo,
            camera=cam_param
        )

        ftp_url_photo = self._remote_rep.upload_photo(path_to_photo)
        self.__remove_photo_from_buffer(path_to_photo)

        form = ApplicationForm(
            car_plate=save_form.car_plate,
            counterparty=save_form.counterparty,
            operation_type=save_form.operation_type,
            equipment_type=save_form.equipment_type,
            camera_type=save_form.camera_type,
            scales_type=save_form.scales_type,
            weight_gross=gross_weight,
            weight_extra=save_form.weight_extra,
            weight_container=save_form.weight_container,
            weight_net=net_weight,
            url_photo=ftp_url_photo,
            date=datetime.now(),
            end_operations=False
        )

        self.__local_rep.save_application(application_form=form)

        return ResultSaveApplication(
            url_photo=ftp_url_photo,
            weight_gross=gross_weight,
            weight_net=net_weight
        )
