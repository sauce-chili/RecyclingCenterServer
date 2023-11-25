from pathlib import Path
from typing import Protocol


class Camera(Protocol):
    def take_photo(self, output_photo_name: str) -> Path:
        ...
