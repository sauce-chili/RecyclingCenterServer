import uuid
from datetime import datetime

from domain.controllers import CameraController, ScaleController
from domain.model.entities import (
    IpCameraParam, ApplicationForm,
    ScalesParam
)
from domain.model.request_schema import (
    SaveApplicationRequest
)
from domain.repository import (
    ApplicationRepository,
    CameraParamsRepository,
    ScalesParamsRepository,
)


class SaveApplicationUseCase:

    def __get_net_weight(self, gross_w: float, container_w: float, extra_w: float):
        if (gross_w == 0):
            return 0

        return gross_w - container_w - (gross_w * (extra_w / 100))

    def __init__(
            self,
            application_repository: ApplicationRepository,
            cameras_repository: CameraParamsRepository,
            scales_repository: ScalesParamsRepository,
            ip_cam_controller: CameraController,
            scales_controller: ScaleController
    ):
        self.__application_rep = application_repository
        self.__cam_rep = cameras_repository
        self.__scales_rep = scales_repository
        self.__ip_cam_controller = ip_cam_controller
        self.__scales_controller = scales_controller

    async def __call__(self, save_request: SaveApplicationRequest):

        scales_param: ScalesParam = self.__scales_rep.get_scales_param_by_name(save_request.scales_type)
        gross_weight: float = self.__scales_controller.weight(scales_param).result

        net_weight: float = self.__get_net_weight(
            gross_w=gross_weight,
            container_w=save_request.weight_container,
            extra_w=save_request.weight_extra
        )

        cam_name: str | None = save_request.camera_type

        cam_param: IpCameraParam

        '''
        In the first version of the project there were supposed to be 2 cameras types, 
        but then the decision was made to mount only one, so the `camera_type` field is passing empty
        '''
        if cam_name is None:
            cam_param = self.__cam_rep.get_cameras_param_list()[0]
            cam_name = cam_param.name
        else:
            cam_param: IpCameraParam = self.__cam_rep.get_camera_param_by_name(cam_name)

        name_of_photo: str = f'{str(uuid.uuid4())}.png'

        path_to_photo = self.__ip_cam_controller.take_photo(
            output_file_name=name_of_photo,
            camera=cam_param
        )

        form: ApplicationForm = ApplicationForm(
            car_plate=save_request.car_plate,
            counterparty=save_request.counterparty,
            operation_type=save_request.operation_type,
            equipment_type=save_request.equipment_type,
            camera_type=cam_name,
            scales_type=save_request.scales_type,
            weight_gross=gross_weight,
            weight_extra=save_request.weight_extra,
            weight_container=save_request.weight_container,
            weight_net=net_weight,
            local_path_photo=path_to_photo,
            date=datetime.now(),
        )

        save_result = self.__application_rep.save_application(application_form=form)

        return save_result
