from pathlib import Path
import logging
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi import FastAPI, Request
import uvicorn
from domain.model.request_schema import *
from domain.model.response_schema import *
from endpoint_controllers import MainControllerV1


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()

cfg_file = Path("./configurations.yaml")

if not cfg_file.exists():
    logging.error(f"Missing configuration file at path: {str(cfg_file)}")
    raise FileExistsError(f"Missing configuration file at path: {str(cfg_file)}")

main_controller = MainControllerV1(cfg_file)


@app.get("/")
def root():
    return {"msg": "Hello stranger!"}


@app.post("/api/v1/save_application/", response_model=SaveApplicationResponse)
async def save_application(save_application_request: SaveApplicationRequest):
    # body = await save_application_request.body()
    # print(body.decode("utf-8"))
    # print(save_application_request)
    # print(save_application_request)
    responce = await main_controller.save_application(
        save_application_request=save_application_request
    )
    return responce


@app.post("/api/v1/save_application_of_end_weighting/")
async def save_application_of_end_weighting(end_weighting_request: SaveApplicationOfEndWeightingRequest):
    return await main_controller.save_application_of_end_weighting(
        end_weighting_request
    )


@app.get("/api/v1/get_scales_names/")
async def get_scales_name():
    return await main_controller.get_scales_names()


@app.get("/api/v1/get_equipment_list/", response_model=list[EquipmentResponse])
async def get_equipments():
    response = await main_controller.get_equipments_list()
    return response


@app.get("/api/v1/get_orders_list/", response_model=list[OrderResponse])
async def get_orders():
    return await main_controller.get_orders_list()


if __name__ == "__main__":
    try:
        logging.info("Starting the application")
        app.add_middleware(HTTPSRedirectMiddleware)
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
    except Exception as e:
        logging.error(f"Error during application start: {str(e)}")