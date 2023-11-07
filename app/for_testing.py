from pathlib import Path
import serial

from data.source.device.scales import Scales

# from data.source.device.ipcamera import IpCamera
#
# url = 'rtsp://admin:hVtc65pq@192.168.3.65:554/Streaming/Channels/101'
#
# stor_dir = Path('../db/buffer_images/')
# cam = IpCamera(ip_address=url, path_storage_dir=stor_dir)
# cam.take_photo("test1.png")

ser = serial.Serial(
    port='/dev/serial0',  # порт
    baudrate=9600,  # Скорость передачи данных
    parity=serial.PARITY_NONE,  # бит четности
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1  # Таймаут на чтение (в секундах)
)

scales = Scales(serial_port=ser)
weight: float = scales.weigh()
print(weight)
