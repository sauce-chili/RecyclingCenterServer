from datetime import datetime

from domain.model.entities import ClosingApplication
from domain.model.request_schema import SaveApplicationOfEndWeightingRequest
from domain.repository import ApplicationRepository


class SaveApplicationOfEndWeightingUseCase:

    def __init__(
            self,
            application_repository: ApplicationRepository
    ):
        self.__application_rep = application_repository

    def __call__(self, end_weighting_request: SaveApplicationOfEndWeightingRequest):
        closing_app_form: ClosingApplication = ClosingApplication(
            car_plate=end_weighting_request.car_plate,
            counterparty=end_weighting_request.counterparty,
            equipment_type=end_weighting_request.equipment_type,
            operation_type=end_weighting_request.operation_type,
            date=datetime.now()
        )

        self.__application_rep.close_application(closing_app_form)
