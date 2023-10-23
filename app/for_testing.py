from pathlib import Path

from data.source.device.ipcamera import IpCamera

ip = 'rtsp://192.168.3.5'
stor_dir = Path('../db/temp_images/')
cam = IpCamera(ip_address=ip, path_storage_dir=stor_dir)
cam.take_photo("test1.png")
