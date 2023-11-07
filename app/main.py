from pathlib import Path
from fastapi import FastAPI
from app.schemas.response_schema import *
from app.schemas.request_schema import *
from factory_main_controller import provide_MainControllerV1

app = FastAPI()

cfg_file = Path("configurations.yaml")

if not cfg_file.exists():
    raise FileExistsError(f"Missing configuration file at path: {str(cfg_file)}")

main_controller = provide_MainControllerV1(cfg_file)


@app.get("/")
async def root():
    return {"msg": "Hello stranger!"}


@app.post("/api/v1/save_application/", response_model=SaveApplicationResponse)
async def save_application(save_application_request: SaveApplicationRequest):
    # weight = 133.5  # Ваш расчет веса
    # id_record = 123  # Ваша логика для генерации id записи
    # url_photo = "https://example.com/photo.jpg"  # Ваша логика для получения URL фотографии
    print(save_application_request)

    return main_controller.save_application(
        save_application_request=save_application_request
    )
