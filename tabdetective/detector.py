from pathlib import Path
from typing import List
from .objects.tables import Tables


class Detector:
    def __init__(self, model: dict):
        self.model: dict = model
        self.tables: Tables = None
        self.text: List[str] = None

    def detect(self, filepath: Path, endoding: str = "utf-8"):
        # to be implemented downstream
        pass

    def _read(self, filepath: Path, endoding: str):
        with open(filepath, "r", encoding=endoding) as f:
            self.text = f.read().splitlines()
