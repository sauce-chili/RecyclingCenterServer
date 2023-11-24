from pathlib import Path
from data.controllers_impl.scales_controller_impl import ScaleControllerImpl
from data.repository_impl import scales_params_repository_impl
from domain.controllers import ScaleController

from domain.model.request_schema import *
from domain.repository import ScalesParamsRepository
from domain.use_cases.factory_usecases.factory_save_application_use_case import FactorySaveApplicationUseCase
from domain.use_cases.factory_usecases.factory_save_application_of_end_weighting_use_case import FactorySaveApplicationOfEndWeightingUseCase


cfg = Path("./configurations.yaml")


scales_param_rep: ScalesParamsRepository = \
            scales_params_repository_impl.YAMLScalesParamsRepository(path_to_yaml=cfg)
scales_controller: ScaleController = ScaleControllerImpl(
            scales_param_list=scales_param_rep.get_scales_param_list()
)

save_use_case = FactorySaveApplicationUseCase(
    yaml_cfg_file=cfg
).provide()

end_weighting_use_case = FactorySaveApplicationOfEndWeightingUseCase(
    yaml_cfg_file=cfg
).provide()

test_preservation_application_from = SaveApplicationRequest(
    car_plate="JKL456",
    counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
    operation_type='inbound',
    equipment_type='notebooks',
    camera_type=None,
    scales_type='Scale 1',
    weight_extra=0.15,
    weight_container=2,
)

result = save_use_case(test_preservation_application_from)

# # print(result)

# # test_end_weighting_applicaton_request = SaveApplicationOfEndWeightingRequest(
# #     car_plate="DGS456",
# #     counterparty="Ромашка",
# #     operation_type='inbound',
# #     equipment_type='phone'
# # )

# # end_weighting_use_case(test_end_weighting_applicaton_request)

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

# print(result)


# while 1:
#     w = scales_controller.weight(
#         scales_param_rep.get_scales_param_by_name('Scale 1')
#     )

#     print(w)

# import re

# valid_mask_len: int = 11
# valid_encoded_data_mask = r'w[wn]\d{3}\.\d{3}kg'

# def is_valid_encoded_data(data: str):
#         if len(data) != valid_mask_len:
#             return False
        
#         return re.fullmatch(valid_encoded_data_mask, data) is not None

# print(is_valid_encoded_data('ww123.456kg')) # T
# print(is_valid_encoded_data('wn322.522kg')) # T
# print(is_valid_encoded_data('wn100.022kg')) # T
# print(is_valid_encoded_data('ww000.000kg')) # T
# print(is_valid_encoded_data('w23.456kg')) # F

# print(is_valid_encoded_data('wn23.456kg')) # F
# print(is_valid_encoded_data('w23.456')) # F
# print(is_valid_encoded_data('wn23456kg')) # F