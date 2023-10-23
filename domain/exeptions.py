class CameraNotAvailable(Exception):

    def __init__(self, msg: str):
        super(msg)
        self.msg = msg
