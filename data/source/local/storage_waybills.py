from typing import Protocol
from .model import ApplicationDto


class StorageWaybills(Protocol):

    def save(self):
        ...

    def get_all(self) -> list[ApplicationDto]:
        ...
