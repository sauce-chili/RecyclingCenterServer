from pathlib import Path

from domain.model.request_schema import *
from domain.use_cases.factory_usecases.factory_save_application_use_case import FactorySaveApplicationUseCase
from domain.use_cases.factory_usecases.factory_save_application_of_end_weighting_use_case import FactorySaveApplicationOfEndWeightingUseCase

cfg = Path("./configurations.yaml")

save_use_case = FactorySaveApplicationUseCase(
    yaml_cfg_file=cfg
).provide()

end_weighting_use_case = FactorySaveApplicationOfEndWeightingUseCase(
    yaml_cfg_file=cfg
).provide()

# test_preservation_application_from = SaveApplicationRequest(
#     car_plate="JKL456",
#     counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
#     operation_type='inbound',
#     equipment_type='notebooks',
#     camera_type=None,
#     scales_type='Scale 2',
#     weight_extra=0.15,
#     weight_container=2,
# )

# result = save_use_case(test_preservation_application_from)

# print(result)

# test_end_weighting_applicaton_request = SaveApplicationOfEndWeightingRequest(
#     car_plate="DGS456",
#     counterparty="Ромашка",
#     operation_type='inbound',
#     equipment_type='phone'
# )

# end_weighting_use_case(test_end_weighting_applicaton_request)

test_preservation_application_from = SaveApplicationRequest(
    car_plate="DGS456",
    counterparty="Ромашка",
    operation_type='inbound',
    equipment_type='phone',
    camera_type=None,
    scales_type='Весы 1',
    weight_extra=0,
    weight_container=2,
)

result = save_use_case(test_preservation_application_from)

print(result)
