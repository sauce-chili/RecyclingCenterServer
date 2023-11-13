from typing import Protocol
from serial import Serial, SerialException
from domain.exeptions import ScalesUnavailable, WeightDecodingException


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

        data: str | None = None

        try:
            data = self.__ser_port.readline()
        except SerialException as ser_exp:
            raise ScalesUnavailable(f"Scales are unavailable. Cannot read data from port {self.__ser_port}")

        encoded_data: str | None = None

        try:
            for _ in range(5):
                encoded_data = data.decode(self.__encoding).strip("\r\n")
                break    
        except:
            pass

        if encoded_data is None:
            exp = WeightDecodingException(msg="Cannot decode weight value", uncoded_data=data)
            raise exp

        result: float = 0.0
        if encoded_data != '':
            result = self.__get_weight_value(encoded_data)

        return result
