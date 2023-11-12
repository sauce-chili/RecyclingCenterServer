import unittest
import serial
from data.source.device.scales import Scales

'''
dmesg | grep tty

'''
class SimpleGettingDataFromScales(unittest.TestCase):
    ser = serial.Serial(
        port='/dev/serial0',  # порт
        baudrate=9600,  # Скорость передачи данных
        parity=serial.PARITY_NONE,  # бит четности
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1  # Таймаут на чтение (в секундах)
    )

    __scales = Scales(ser)

    def test_something(self):
        weight: float = self.__scales.weigh()

        print(weight)

        self.assertTrue(weight is float)  # add assertion here


if __name__ == '__main__':
    unittest.main()
