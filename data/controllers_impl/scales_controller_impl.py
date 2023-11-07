from pathlib import Path
import serial

from domain.controllers import *
from domain.exeptions import *
from domain.repository import ScalesParamsRepository
from data.source.device.scales import (Scales, Sci12Scales)


class ScaleControllerImpl(ScaleController):

    def __get_default_serial(self, port: str) -> serial.Serial:
        return serial.Serial(
            port=port,  # порт
            baudrate=9600,  # Скорость передачи данных
            parity=serial.PARITY_NONE,  # бит четности
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1  # Таймаут на чтение (в секундах)
        )

    def __get_default_scales(self, port: str) -> Scales:
        return Sci12Scales(serial_port=self.__get_default_serial(port=port))

    def __init__(self, scales_param_list: list[ScalesParam]):
        self.__scales: dict[ScalesParam, Scales] = {
            param: self.__get_default_scales(port=param.port)
            for param in scales_param_list
        }

    def weight(self, scales_param: ScalesParam) -> WeighingResult:
        weigh_result: float = self.__scales[scales_param].weigh()

        return WeighingResult(result=weigh_result)
