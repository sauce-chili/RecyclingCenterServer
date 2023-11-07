from pathlib import Path

from domain.models import PreservationApplicationForm
from domain.use_cases.factory_usecases.factory_save_application_use_case import FactorySaveApplicationUseCase

cfg = Path("configurations.yaml")

save_use_case = FactorySaveApplicationUseCase(
    yaml_cfg_file=cfg
).provide()

test_preservation_application_from = PreservationApplicationForm(
    car_plate="JKL456",
    counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
    operation_type='inbound',
    equipment_type='notebooks',
    camera_type=None,
    scales_type='scales 2',
    weight_extra=0.15,
    weight_container=2,
)

result = save_use_case(test_preservation_application_from)

print(result)
