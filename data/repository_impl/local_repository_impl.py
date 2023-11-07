from domain.models import ApplicationForm
from domain.repository import ApplicationRepository

from data.source.local.model import PreservationApplicationDto
from data.source.local.storage_applications import StorageApplications
from data.utils.mappers import map_PreservationApplicationForm_to_PreservationActiveApplicationDto


class LocalRepositoryImpl(ApplicationRepository):

    def __init__(
            self,
            stor_applications: StorageApplications,
    ):
        self.__stor_applications = stor_applications

    # TODO написать метод для возврата записи конца взвешивания

    def save_application(self, application_form: ApplicationForm) -> None:
        dto: PreservationApplicationDto = \
            map_PreservationApplicationForm_to_PreservationActiveApplicationDto(application_form
                                                                                )
        self.__stor_applications.save(dto)

    def close_application(self, application_from: ApplicationForm) -> None:
        ...

    def __get_closing_applications(self, form: ApplicationForm) -> PreservationApplicationDto:
        return PreservationApplicationDto(
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
            date=form.date.isoformat(),
            end_weighing=1
        )
