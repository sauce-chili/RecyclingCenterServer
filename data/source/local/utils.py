from data.source.local.model import ApplicationStorageDto


def storage_dto_to_csv_line(dto: ApplicationStorageDto, separator: str = '|') -> str:
    # Convert None values to 'NULL'
    fields = [str(getattr(dto, field)) if getattr(dto, field) is not None else 'NULL' for field in
              dto.__annotations__.keys()]

    # Create a CSV line using the specified separator
    csv_line = f"{separator.join(fields)}"

    return csv_line + '\n'

# app_form = ApplicationForm(car_plate="ABC123", counterparty="CompanyX", operation_type="Delivery",
#                            equipment_type="Truck", camera_type=None, scales_type="Digital",
#                            weight_gross=None, weight_extra=200.0, weight_container=1000.0,
#                            weight_net=3800.0, url_photo="http://example.com/photo.jpg",
#                            date=datetime.now(), end_operations=False)

# csv_line = application_from_to_csv_line(app_form)
# print(csv_line)
