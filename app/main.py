from fastapi import FastAPI
from app.schemas.response_schema import *
from app.schemas.request_schema import *

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "Hello stranger!"}


@app.post("/api/v1/save_application/", response_model=SaveApplicationResponse)
async def save_application(save_application_request: SaveApplicationRequest):
    weight = 133.5  # Ваш расчет веса
    id_record = 123  # Ваша логика для генерации id записи
    url_photo = "https://example.com/photo.jpg"  # Ваша логика для получения URL фотографии
    print(save_application_request)

    # Возвращаем результаты как экземпляр ApplicationOutput
    return SaveApplicationResponse(weight=weight, id_record=id_record, url_photo=url_photo)
