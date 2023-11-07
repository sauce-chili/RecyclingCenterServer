from typing import Protocol
from .model import ApplicationStorageDto


class StorageWaybills(Protocol):

    def save(self):
        ...

    def get_all(self) -> list[ApplicationStorageDto]:
        ...
