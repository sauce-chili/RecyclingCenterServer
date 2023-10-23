from dataclasses import dataclass
from ftplib import FTP


@dataclass
class ParamFTP:
    host: str
    username: str
    password: str


class ServerFTP:
    _instance = None

    def __new__(cls, ftp_param: ParamFTP):
        if cls._instance is None:
            cls._instance = super(ServerFTP, cls).__new__(cls)
            cls._instance.ftp = FTP(ftp_param.host)
            cls._instance.ftp.login(user=ftp_param.username, passwd=ftp_param.password)
        return cls._instance

    def download_file(self, path_ftp_file: str, path_local_file: str):
        with open(path_local_file, mode='wb') as local_file:
            self.ftp.retrbinary('RETR ' + path_ftp_file, local_file.write)

    def upload_file(self, path_local_file: str, path_ftp_file: str):
        with open(path_local_file, mode='rb') as local_file:
            self.ftp.storbinary('STOR ' + path_ftp_file, local_file)

    def __del__(self):
        self.ftp.quit()
