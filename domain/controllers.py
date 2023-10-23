from typing import Protocol
from pathlib import Path
from domain.models import *


class CameraController(Protocol):

    def take_photo(self, output_file_name: str, camera: IpCameraParam) -> Path:
        ...


class ScaleController(Protocol):

    def weight(self, scales: ScalesParam) -> WeighingResult:
        ...
