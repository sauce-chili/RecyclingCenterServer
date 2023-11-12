class CameraNotAvailableException(Exception):

    def __init__(self, msg: str = None):
        super(msg)
        self.msg = msg
