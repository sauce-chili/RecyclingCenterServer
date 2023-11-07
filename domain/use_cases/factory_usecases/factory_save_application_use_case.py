from pathlib import Path

from data.controllers_impl import (
    camera_controller_impl,
    scales_controller_impl
)
from data.factory_repository.factory_remote_repository import FactoryFtpRemoteRepository
from data.repository_impl import (
    scales_params_repository_impl,
    camera_params_repository_impl,
    local_repository_impl
)
from data.source.local.factory_storage.factory_storage_applications import FactorySQLiteStorageApplication
from domain.controllers import (
    CameraController,
    ScaleController
)
from domain.repository import (
    ApplicationRepository,
    RemoteRepository,
    CameraParamsRepository,
    ScalesParamsRepository,
)
from domain.use_cases.save_application_use_case import SaveApplicationUseCase
from domain.utils import get_database_param


class FactorySaveApplicationUseCase:

    def __init__(self, yaml_cfg_file: Path):
        if not yaml_cfg_file.exists():
            raise FileExistsError(f"Config file {yaml_cfg_file} doesn't exist")

        self.__cfg = yaml_cfg_file

    def provide(self) -> SaveApplicationUseCase:
        scales_param_rep: ScalesParamsRepository = \
            scales_params_repository_impl.YAMLScalesParamsRepository(path_to_yaml=self.__cfg)
        camera_param_rep: CameraParamsRepository = \
            camera_params_repository_impl.YAMLCameraParamsRepository(path_to_yaml=self.__cfg)

        db_param = get_database_param(yaml_config_file=self.__cfg)

        cam_controller: CameraController = camera_controller_impl.IPCameraController(
            path_storage_dir=db_param.image_buffer_folder_path,
            cameras_param=camera_param_rep.get_cameras_param_list()
        )

        scales_controller: ScaleController = scales_controller_impl.ScaleControllerImpl(
            scales_param_list=scales_param_rep.get_scales_param_list()
        )

        remote_rep: RemoteRepository = FactoryFtpRemoteRepository(
            yaml_cfg_path=self.__cfg
        ).provide_remote_repository()

        application_storage = FactorySQLiteStorageApplication(yaml_cfg_path=self.__cfg).provide_storage_application()

        local_rep: ApplicationRepository = local_repository_impl.LocalRepositoryImpl(
            stor_applications=application_storage
        )

        return SaveApplicationUseCase(
            local_repository=local_rep,
            remote_repository=remote_rep,
            cameras_repository=camera_param_rep,
            scales_repository=scales_param_rep,
            ip_cam_controller=cam_controller,
            scales_controller=scales_controller
        )
