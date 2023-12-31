from typing import Protocol
from serial import Serial


class Scales(Protocol):

    def weigh(self) -> float:
        ...


class Sci12Scales(Scales):
    __encoding = 'utf-8'

    def __init__(self, serial_port: Serial):
        self.__ser_port: Serial = serial_port

    def __cut_type_of_weight(self, weight: str) -> str:
        return weight[2:]

    def __cut_unit_of_measurement(self, weight: str) -> str:
        return weight[:-2]

    def __get_weight_value(self, data: str) -> float:
        tmp = self.__cut_type_of_weight(data)
        weight_value_str = self.__cut_unit_of_measurement(tmp)

        weight = float(weight_value_str)

        return weight

    def weigh(self) -> float:
        data = self.__ser_port.readline()

        encoded_data = data.decode(self.__encoding).strip("\r\n")

        result: float = 0.0
        if encoded_data != '':
            result = self.__get_weight_value(encoded_data)

        return result
