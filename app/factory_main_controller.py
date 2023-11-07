from pathlib import Path

from app.endpoint_controllers import MainControllerV1
from domain.use_cases.save_application_use_case import SaveApplicationUseCase
from domain.use_cases.factory_usecases.factory_save_application_use_case import FactorySaveApplicationUseCase


def provide_MainControllerV1(yaml_cfg_path: Path):
    save_app_use_case: SaveApplicationUseCase = FactorySaveApplicationUseCase(
        yaml_cfg_file=yaml_cfg_path
    ).provide()

    return MainControllerV1(
        save_application_use_case=save_app_use_case
    )
