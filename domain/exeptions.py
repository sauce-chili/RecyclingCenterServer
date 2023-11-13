class CameraNotAvailableException(Exception):

    def __init__(self, msg: str = None):
        super(msg)
        self.msg = msg

class ScalesException(Exception):
    pass

class ScalesUnavailable(ScalesException):
    pass

class WeightDecodingException(ScalesException):
    def __init__(self, msg: str | None = None, uncoded_data: str | None = None) -> None:
        super().__init__()
        self.msg = msg
        self.uncoded_data = uncoded_data