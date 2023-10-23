from data.source.local.model import ApplicationDto
from domain.models import ApplicationForm


def map_ApplicationDto_to_ApplicationForm(app_dto: ApplicationDto) -> ApplicationForm:
    return ApplicationForm(
        id=app_dto.id,
        weighing_order=app_dto.weighing_order,
        source=app_dto.source,
        destination=app_dto.destination,
        type_operation=app_dto.type_operation,
        camera_type=app_dto.camera_type,
        scales_type=app_dto.scales_type,
        weight=app_dto.weight,
        url_photo=app_dto.url_photo
    )

