from domain.models import PreservationApplicationForm
from app.schemas.request_schema import SaveApplicationRequest


def map_SaveApplicationRequest_to_PreservationApplicationForm(request: SaveApplicationRequest):
    return PreservationApplicationForm(
        car_plate=request.car_plate,
        counterparty=request.counterparty,
        operation_type=request.operation_type,
        equipment_type=request.equipment_type,
        camera_type=None,
        scales_type=request.scales_type,
        weight_extra=request.weight_extra,
        weight_container=request.weight_container
    )
