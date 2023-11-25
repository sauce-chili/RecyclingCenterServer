import re

from typing import Protocol
from serial import Serial, SerialException
from domain.exeptions import ScalesUnavailable, WeightDecodingException


class Scales(Protocol):

    def weigh(self) -> float:
        ...


class Sci12Scales(Scales):
    __encoding = 'utf-8'

    __valid_encoded_data_mask = r'w[wn]\d*\.\d*kg$'

    def __init__(self, serial_port: Serial):
        self.__ser_port: Serial = serial_port

    def __cut_type_of_weight(self, weight: str) -> str:
        return weight[2:]

    def __cut_unit_of_measurement(self, weight: str) -> str:
        return weight[:-2]

    def __get_weight_value(self, data: str) -> float:
        tmp = self.__cut_type_of_weight(data)
        weight_value_str = self.__cut_unit_of_measurement(tmp)

        # print(f"Weight value after cutting: {weight_value_str}")
        weight = float(weight_value_str)

        return weight

    def __is_valid_encoded_data(self, data: str):
        return re.fullmatch(self.__valid_encoded_data_mask, data) is not None

    def weigh(self) -> float:

        data: str | None = None

        try:
            self.__ser_port.reset_input_buffer()
            data = self.__ser_port.readline()
            # print(self.__ser_port.in_waiting)
        except SerialException as ser_exp:
            raise ScalesUnavailable(f"Scales are unavailable. Cannot read data from port {self.__ser_port}")

        encoded_data: str | None = None

        for _ in range(20):
            try:
                d = data.decode(self.__encoding).strip("\r\n")
                # print(f'Encoded data: {d}')
                if self.__is_valid_encoded_data(d):
                    encoded_data = d
                    break
            except:
                pass
        else:
            exp = WeightDecodingException(msg="Cannot decode weight value", uncoded_data=data)
            raise exp

        result: float = 0.0
        if encoded_data != '':
            result = self.__get_weight_value(encoded_data)

        return result
