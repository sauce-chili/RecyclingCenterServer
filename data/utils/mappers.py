# deprecated

# def map_ApplicationStorageDto_to_ApplicationForm(app_dto: ApplicationStorageDto) -> ApplicationForm:
#     return ApplicationForm(
#         id=app_dto.id,
#         weighing_order=app_dto.weighing_order,
#         source=app_dto.source,
#         destination=app_dto.destination,
#         type_operation=app_dto.operation_type,
#         camera_type=app_dto.camera_type,
#         scales_type=app_dto.scales_type,
#         weight=app_dto.weight_gross,
#         url_photo=app_dto.url_photo
#     )


# def map_PreservationApplicationForm_to_PreservationActiveApplicationDto(form: ApplicationForm) \
#         -> PreservationApplicationDto:
#     return PreservationApplicationDto(
#         car_plate=form.car_plate,
#         counterparty=form.counterparty,
#         operation_type=form.operation_type,
#         equipment_type=form.equipment_type,
#         camera_type=form.camera_type,
#         scales_type=form.scales_type,
#         weight_gross=form.weight_gross,
#         weight_extra=form.weight_extra,
#         weight_net=form.weight_net,
#         weight_container=form.weight_container,
#         url_photo=form.local_path_photo,
#         date=form.date.isoformat(),
#
#     )
