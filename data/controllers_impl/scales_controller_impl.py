from data.source.device.ipcamera import IpCamera
from domain.controllers import *
from domain.exeptions import *
from pathlib import Path


class ScaleControllerImpl(ScaleController):

    def weight(self, scales: ScalesParam) -> WeighingResult: raise NotImplementedError()