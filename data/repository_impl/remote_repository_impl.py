from pathlib import Path

from data.source.remote.server_ftp import ServerFTP
from domain.repository import RemoteRepository
from domain.models import DatabaseParam


class FtpRemoteRepository(RemoteRepository):

    def __init__(self, server_ftp: ServerFTP, db_param: DatabaseParam):
        self.__server = server_ftp
        self.__db_param = db_param

    def update_db(self) -> None:
        self.__server.upload_file(
            path_local_file=self.__db_param.db_path,
            path_ftp_file=self.__db_param.db_remote_path
        )

    def upload_photo(self, path_to_photo: Path) -> str:
        ftp_path_file = self.__db_param.image_buffer_folder_remote_path / path_to_photo.name

        self.__server.upload_file(
            path_local_file=path_to_photo,
            path_ftp_file=ftp_path_file
        )

        return self.__server.get_url_to_file(str(ftp_path_file))

# from data.source.remote.server_ftp import ServerFTP, get_ftp_server_param
# from domain.utils import get_database_param
#
# ftp_ser_param = get_ftp_server_param(Path("../../app/configurations.yaml"))
# ser = ServerFTP(ftp_ser_param)
# db_param = get_database_param(Path("../../app/configurations.yaml"))
#
# rem_rep = RemoteRepositoryImpl(server_ftp=ser, db_param=db_param)
# rem_rep.upload_photo(Path("D:\\programms\\Python\\RecyclingCenterServer\\db\\buffer_images\\test1.png"))
