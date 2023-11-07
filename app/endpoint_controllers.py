from domain.use_cases.save_application_use_case import SaveApplicationUseCase
from domain.use_cases.use_cases import *

from app.schemas.response_schema import SaveApplicationResponse

from domain.models import *
from app.schemas.request_schema import SaveApplicationRequest
from app.mappers import map_SaveApplicationRequest_to_PreservationApplicationForm


class MainControllerV1:

    def __init__(
            self,
            save_application_use_case: SaveApplicationUseCase
    ):
        self.__save_app_usecase = save_application_use_case

    async def save_application(self, save_application_request: SaveApplicationRequest):
        app_from = map_SaveApplicationRequest_to_PreservationApplicationForm(save_application_request)

        result_save: ResultSaveApplication = await self.__save_app_usecase(save_form=app_from)

        return SaveApplicationResponse(
            weight_gross=result_save.weight_gross,
            weight_net=result_save.weight_net,
            url_photo=result_save.url_photo
        )
