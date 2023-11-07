from typing import Protocol
from .model import PreservationApplicationDto, ApplicationStorageDto


class StorageApplications(Protocol):

    def save(self, application_dto: PreservationApplicationDto) -> None:
        ...

    def get_all(self) -> list[ApplicationStorageDto]:
        ...

    def remove_storage(self) -> None:
        ...

    def count_records(self) -> int:
        ...
