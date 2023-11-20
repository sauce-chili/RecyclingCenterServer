from pydantic import BaseModel



class SaveApplicationRequest(BaseModel):
    car_plate: str
    counterparty: str
    operation_type: str
    equipment_type: str
    camera_type: str | None
    scales_type: str
    weight_extra: float
    weight_container: float



class SaveApplicationOfEndWeightingRequest(BaseModel):
    car_plate: str
    counterparty: str
    operation_type: str
    equipment_type: str
