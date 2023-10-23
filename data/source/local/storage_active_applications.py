from typing import Protocol
from .model import SaveActiveApplicationDto, ActiveApplicationDto


class TemporaryStorageActiveApplications(Protocol):

    def save(self, application_dto: SaveActiveApplicationDto) -> None:
        ...

    def get_all(self) -> list[ActiveApplicationDto]:
        ...

    def clear(self) -> None:
        ...

    def count_records(self) -> int:
        ...
